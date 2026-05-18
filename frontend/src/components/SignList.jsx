import React, { useEffect, useState } from 'react';
import { motion } from 'framer-motion';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';

// Emoji mapping for visual appeal
const SIGN_EMOJI = {
  hello: '👋', yes: '✅', no: '❌', thankyou: '🙏', please: '🤲',
  sorry: '😔', help: '🆘', good: '👍', bad: '👎', stop: '✋',
  iloveyou: '❤️', goodmorning: '🌅', goodnight: '🌙', howareyou: '🤔', fine: '😊',
  eat: '🍽️', drink: '🥤', sleep: '😴', come: '🫵', go: '🚶',
  A: '🅰️', B: '🅱️', C: '©️', D: '🔷', E: '📧',
  F: '🎵', G: '🎸', H: '🏥', I: 'ℹ️', J: '🎭',
  '1': '1️⃣', '2': '2️⃣', '3': '3️⃣', '4': '4️⃣', '5': '5️⃣',
  '6': '6️⃣', '7': '7️⃣', '8': '8️⃣', '9': '9️⃣', '10': '🔟',
};

const CATEGORIES = {
  'Common Phrases':  ['hello','yes','no','thankyou','please','sorry','help','good','bad','stop'],
  'Expressions':     ['iloveyou','goodmorning','goodnight','howareyou','fine'],
  'Actions':         ['eat','drink','sleep','come','go'],
  'Alphabet (A–J)':  ['A','B','C','D','E','F','G','H','I','J'],
  'Numbers 1–10':    ['1','2','3','4','5','6','7','8','9','10'],
};

export default function SignList() {
  const [signs, setSigns]   = useState([]);
  const [query, setQuery]   = useState('');
  const [loading, setLoad]  = useState(true);

  useEffect(() => {
    fetch(`${API_BASE}/api/signs`)
      .then(r => r.json())
      .then(d => setSigns(d.signs || []))
      .catch(() => setSigns(Object.values(CATEGORIES).flat()))
      .finally(() => setLoad(false));
  }, []);

  const filtered = query
    ? signs.filter(s => s.toLowerCase().includes(query.toLowerCase()))
    : null;

  if (loading) return <div className="loading">Loading signs…</div>;

  return (
    <div className="sign-list-page">
      <div className="sl-header">
        <h2>📖 Supported Signs <span className="count-badge">{signs.length}</span></h2>
        <input
          className="search-input"
          placeholder="🔍 Search signs…"
          value={query}
          onChange={e => setQuery(e.target.value)}
        />
      </div>

      {filtered ? (
        <div className="sign-grid">
          {filtered.map((sign, i) => (
            <SignCard key={sign} sign={sign} index={i} />
          ))}
          {filtered.length === 0 && <p className="no-results">No signs match "{query}"</p>}
        </div>
      ) : (
        Object.entries(CATEGORIES).map(([cat, catSigns]) => (
          <div key={cat} className="category-section">
            <h3 className="category-title">{cat}</h3>
            <div className="sign-grid">
              {catSigns.map((sign, i) => (
                <SignCard key={sign} sign={sign} index={i} />
              ))}
            </div>
          </div>
        ))
      )}
    </div>
  );
}

function SignCard({ sign, index }) {
  return (
    <motion.div
      className="sign-card-item"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: index * 0.03, duration: 0.3 }}
      whileHover={{ scale: 1.05, y: -4 }}
    >
      <span className="sc-emoji">{SIGN_EMOJI[sign] || '🤟'}</span>
      <span className="sc-label">{sign}</span>
    </motion.div>
  );
}
