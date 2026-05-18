import React from 'react';

export default function Header() {
  return (
    <header className="app-header">
      <div className="header-logo">
        <span className="logo-icon">🤟</span>
        <div>
          <h1 className="logo-title">SignAI</h1>
          <p className="logo-sub">Real-time Sign Language Translator</p>
        </div>
      </div>
      <div className="header-badge">
        <span className="badge">40 Signs</span>
        <span className="badge badge-ai">AI Powered</span>
      </div>
    </header>
  );
}
