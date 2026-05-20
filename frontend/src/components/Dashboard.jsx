import { useState, useEffect } from 'react';
import { signOut } from 'firebase/auth';
import { auth } from '../firebase';

function Dashboard({ user }) {
  const [cards, setCards] = useState([]);
  const [collection, setCollection] = useState([]);
  const [masterMode, setMasterMode] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    // In a real app, this would fetch from our Rust backend
    // For now, we mock some creatures just like in the python script to show the UI
    const mockCreatures = [
      { id: '1', number: '001', name: 'Montigo' },
      { id: '2', number: '002', name: 'Brukey' },
      { id: '3', number: '003', name: 'Felixir' },
      { id: '4', number: '004', name: 'Daereap' },
      { id: '5', number: '005', name: 'Naryu' },
    ];
    setCards(mockCreatures);
    setLoading(false);
  }, []);

  const handleLogout = () => {
    signOut(auth);
  };

  const getQuantity = (cardId, variant) => {
    const found = collection.find(c => c.cardId === cardId && c.variant === variant);
    return found ? found.quantity : 0;
  };

  const incrementQuantity = (cardId, variant) => {
    // Mocking API call
    setCollection(prev => {
      const existing = prev.find(c => c.cardId === cardId && c.variant === variant);
      if (existing) {
        return prev.map(c => 
          c.cardId === cardId && c.variant === variant 
            ? { ...c, quantity: c.quantity + 1 }
            : c
        );
      }
      return [...prev, { cardId, variant, quantity: 1 }];
    });
  };

  if (loading) return <div className="layout-container">Loading Dashboard...</div>;

  return (
    <div className="layout-container">
      <div className="app-header">
        <div>
          <h1 className="title-gradient">Elemental Checklist</h1>
          <p style={{ color: 'var(--text-secondary)' }}>Welcome, {user.email}</p>
        </div>
        <div style={{ display: 'flex', gap: '16px', alignItems: 'center' }}>
          <label className="checkbox-wrapper">
            <input 
              type="checkbox" 
              checked={masterMode} 
              onChange={(e) => setMasterMode(e.target.checked)} 
            />
            <span style={{ color: 'var(--text-primary)' }}>Master Set Mode</span>
          </label>
          <button className="btn-primary" onClick={handleLogout}>Log Out</button>
        </div>
      </div>

      <div className="card-grid">
        {cards.map(card => (
          <div key={card.id} className="creature-card">
            <div className="creature-info">
              <span className="creature-number">#{card.number}</span>
              <span className="creature-name">{card.name}</span>
            </div>
            <div className="card-actions">
              <div style={{ display: 'flex', flexDirection: 'column', gap: '8px' }}>
                <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                  <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Reg</span>
                  <button 
                    onClick={() => incrementQuantity(card.id, 'Regular')} 
                    style={{ 
                      padding: '4px 8px', 
                      backgroundColor: 'var(--bg-secondary)', 
                      color: 'var(--text-primary)' 
                    }}
                  >
                    {getQuantity(card.id, 'Regular')}
                  </button>
                </div>
                {masterMode && (
                  <div style={{ display: 'flex', alignItems: 'center', gap: '8px' }}>
                    <span style={{ fontSize: '0.8rem', color: 'var(--text-secondary)' }}>Holo</span>
                    <button 
                      onClick={() => incrementQuantity(card.id, 'Holo')} 
                      style={{ 
                        padding: '4px 8px',
                        backgroundColor: 'var(--bg-secondary)', 
                        color: 'var(--text-primary)'
                      }}
                    >
                      {getQuantity(card.id, 'Holo')}
                    </button>
                  </div>
                )}
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  );
}

export default Dashboard;
