import React from 'react';

const STATUS_CONFIG = {
  connected:    { color: '#22c55e', label: 'Connected',    dot: '●' },
  disconnected: { color: '#f59e0b', label: 'Disconnected', dot: '●' },
  error:        { color: '#ef4444', label: 'Error',        dot: '●' },
};

export default function StatusBar({ wsStatus, handDetected }) {
  const cfg = STATUS_CONFIG[wsStatus] || STATUS_CONFIG.disconnected;

  return (
    <div className="status-bar">
      <span style={{ color: cfg.color }} className="status-dot">
        {cfg.dot} {cfg.label}
      </span>
      <span className={`hand-indicator ${handDetected ? 'active' : ''}`}>
        ✋ {handDetected ? 'Hand Detected' : 'No Hand'}
      </span>
    </div>
  );
}
