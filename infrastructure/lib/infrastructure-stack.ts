import * as cdk from 'aws-cdk-lib';
import { Construct } from 'constructs';
import * as ec2 from 'aws-cdk-lib/aws-ec2';
import * as rds from 'aws-cdk-lib/aws-rds';
import * as secretsmanager from 'aws-cdk-lib/aws-secretsmanager';

export class InfrastructureStack extends cdk.Stack {
  constructor(scope: Construct, id: string, props?: cdk.StackProps) {
    super(scope, id, props);

    // 1. Create a VPC for the EC2 instance and Aurora Serverless v2 database
    const vpc = new ec2.Vpc(this, 'ElementalVpc', {
      maxAzs: 2,
      natGateways: 0,
      subnetConfiguration: [
        {
          cidrMask: 24,
          name: 'Public',
          subnetType: ec2.SubnetType.PUBLIC,
        },
        {
          cidrMask: 24,
          name: 'Isolated',
          subnetType: ec2.SubnetType.PRIVATE_ISOLATED,
        }
      ],
    });

    // 2. Create the Security Group for EC2
    const ec2Sg = new ec2.SecurityGroup(this, 'Ec2SecurityGroup', {
      vpc,
      description: 'Allow HTTP/HTTPS traffic to EC2',
      allowAllOutbound: true,
    });
    ec2Sg.addIngressRule(ec2.Peer.anyIpv4(), ec2.Port.tcp(80), 'Allow HTTP traffic');
    ec2Sg.addIngressRule(ec2.Peer.anyIpv4(), ec2.Port.tcp(443), 'Allow HTTPS traffic');
    ec2Sg.addIngressRule(ec2.Peer.anyIpv4(), ec2.Port.tcp(22), 'Allow SSH traffic');

    // 3. Database Credentials using Secrets Manager
    const dbCredentialsSecret = new secretsmanager.Secret(this, 'DatabaseSecret', {
      generateSecretString: {
        secretStringTemplate: JSON.stringify({ username: 'postgres' }),
        generateStringKey: 'password',
        excludePunctuation: true,
      },
    });

    // 4. Create Aurora Serverless v2 PostgreSQL Cluster
    const dbCluster = new rds.DatabaseCluster(this, 'ElementalAuroraCluster', {
      engine: rds.DatabaseClusterEngine.auroraPostgres({ version: rds.AuroraPostgresEngineVersion.VER_17_9 }),
      serverlessV2MinCapacity: 0.5,
      serverlessV2MaxCapacity: 1.0,
      writer: rds.ClusterInstance.serverlessV2('Writer'),
      vpc,
      vpcSubnets: { subnetType: ec2.SubnetType.PRIVATE_ISOLATED },
      credentials: rds.Credentials.fromSecret(dbCredentialsSecret),
      defaultDatabaseName: 'elemental_checklist',
      storageEncrypted: true,
    });

    // Allow EC2 to access Aurora on port 5432
    dbCluster.connections.allowDefaultPortFrom(ec2Sg, 'Allow EC2 access to Aurora Serverless');

    // 5. Create the EC2 Instance
    const keyPair = ec2.KeyPair.fromKeyPairName(this, 'ElementalKeyPair', 'elemental-checklist-key');

    const ec2Instance = new ec2.Instance(this, 'ElementalWebInstance', {
      vpc,
      vpcSubnets: { subnetType: ec2.SubnetType.PUBLIC },
      instanceType: ec2.InstanceType.of(ec2.InstanceClass.T4G, ec2.InstanceSize.NANO),
      machineImage: ec2.MachineImage.latestAmazonLinux2023({ cpuType: ec2.AmazonLinuxCpuType.ARM_64 }),
      securityGroup: ec2Sg,
      keyPair: keyPair,
    });

    // Assign an Elastic IP to the EC2 Instance
    const eip = new ec2.CfnEIP(this, 'ElementalEIP', {
      instanceId: ec2Instance.instanceId,
    });

    // Grant EC2 permission to read the database secret
    dbCredentialsSecret.grantRead(ec2Instance);

    // 6. User Data Script: Production setup with Caddy and systemd
    ec2Instance.addUserData(
      '#!/bin/bash',
      '# Install dependencies',
      'dnf update -y',
      'dnf install -y jq',
      
      '# Fetch Database Credentials from Secrets Manager',
      `SECRET_JSON=$(aws secretsmanager get-secret-value --secret-id ${dbCredentialsSecret.secretArn} --region ${cdk.Stack.of(this).region} --query SecretString --output text)`,
      'DB_USER=$(echo $SECRET_JSON | jq -r .username)',
      'DB_PASS=$(echo $SECRET_JSON | jq -r .password)',
      `DB_HOST=${dbCluster.clusterEndpoint.hostname}`,
      'DATABASE_URL="postgres://${DB_USER}:${DB_PASS}@${DB_HOST}:5432/elemental_checklist"',

      '# Create app directory and .env file',
      'mkdir -p /home/ec2-user/elemental/public',
      'echo "DATABASE_URL=$DATABASE_URL" > /home/ec2-user/elemental/.env',
      'chown -R ec2-user:ec2-user /home/ec2-user/elemental',

      '# Install Caddy for automatic HTTPS and reverse proxying',
      'dnf install -y \'dnf-command(copr)\'',
      'dnf copr enable -y @caddy/caddy',
      'dnf install -y caddy',

      '# Configure Caddyfile',
      'cat << \'EOF\' > /etc/caddy/Caddyfile',
      'elementalchecklist.com, www.elementalchecklist.com {',
      '    handle /api/* {',
      '        reverse_proxy 127.0.0.1:8000',
      '    }',
      '    handle {',
      '        root * /home/ec2-user/elemental/public',
      '        file_server',
      '        try_files {path} /index.html',
      '    }',
      '}',
      'EOF',
      'systemctl enable caddy',
      'systemctl restart caddy',

      '# Configure systemd service for the Rust backend',
      'cat << \'EOF\' > /etc/systemd/system/elemental.service',
      '[Unit]',
      'Description=Elemental Checklist Rust Backend',
      'After=network.target',
      '',
      '[Service]',
      'User=ec2-user',
      'WorkingDirectory=/home/ec2-user/elemental',
      'ExecStart=/home/ec2-user/elemental/backend',
      'Restart=always',
      'Environment="ROCKET_ADDRESS=127.0.0.1"',
      'Environment="ROCKET_PORT=8000"',
      'EnvironmentFile=/home/ec2-user/elemental/.env',
      '',
      '[Install]',
      'WantedBy=multi-user.target',
      'EOF',
      'systemctl daemon-reload',
      'systemctl enable elemental.service',
      '# The service might fail initially until the binary is copied over, which is expected.',

      '# Allow ec2-user to restart the service without a password',
      'echo "ec2-user ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart elemental.service" > /etc/sudoers.d/elemental'
    );

    // Outputs
    new cdk.CfnOutput(this, 'ElasticIP', {
      value: eip.ref,
      description: 'The Elastic IP address of the EC2 instance',
    });

    new cdk.CfnOutput(this, 'DatabaseEndpoint', {
      value: dbCluster.clusterEndpoint.hostname,
      description: 'The hostname of the Aurora cluster',
    });

    new cdk.CfnOutput(this, 'DatabaseSecretArn', {
      value: dbCredentialsSecret.secretArn,
      description: 'The ARN of the database credentials secret',
    });
  }
}
