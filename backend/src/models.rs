use serde::{Deserialize, Serialize};
use uuid::Uuid;
use chrono::{DateTime, Utc};
use sqlx::FromRow;

#[derive(Serialize, Deserialize, FromRow)]
pub struct User {
    pub firebase_uid: String,
    pub username: String,
    pub created_at: DateTime<Utc>,
}

#[derive(Serialize, Deserialize, FromRow)]
pub struct Set {
    pub id: Uuid,
    pub name: String,
    pub release_date: Option<chrono::NaiveDate>,
    pub total_cards: i32,
}

#[derive(Serialize, Deserialize, FromRow)]
pub struct Card {
    pub id: Uuid,
    pub set_id: Uuid,
    pub number: String,
    pub name: String,
    pub image_url: Option<String>,
}

#[derive(Serialize, Deserialize, FromRow)]
pub struct Collection {
    pub id: Uuid,
    pub firebase_uid: String,
    pub card_id: Uuid,
    pub variant: String, // "Regular", "Holo"
    pub quantity: i32,
    pub acquired_at: DateTime<Utc>,
}

#[derive(Serialize, Deserialize)]
pub struct AddCardRequest {
    pub card_id: Uuid,
    pub variant: String,
}
