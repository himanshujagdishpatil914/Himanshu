import React, { useRef, useEffect, useCallback, useState } from 'react';
import Webcam from 'react-webcam';

const WS_URL = process.env.REACT_APP_WS_URL || 'ws://localhost:8000/ws/predict';
const FPS    = 15;   // frames per second sent to backend

export default function Camera({ onPrediction, onStatusChange }) {
  const webcamRef = useRef(null);
  const wsRef     = useRef(null);
  const timerRef  = useRef(null);
  const [active, setActive]     = useState(false);
  const [mirror, setMirror]     = useState(true);
  const [camError, setCamError] = useState(null);

  // ── WebSocket ──────────────────────────────────────────────────────────────
  const connectWS = useCallback(() => {
    if (wsRef.current?.readyState === WebSocket.OPEN) return;

    const ws = new WebSocket(WS_URL);
    wsRef.current = ws;

    ws.onopen  = () => { onStatusChange('connected');    console.log('[WS] connected'); };
    ws.onclose = () => { onStatusChange('disconnected'); console.log('[WS] closed');    };
    ws.onerror = () => { onStatusChange('error');        console.log('[WS] error');     };
    ws.onmessage = (evt) => {
      try { onPrediction(JSON.parse(evt.data)); } catch (_) {}
    };
  }, [onPrediction, onStatusChange]);

  const disconnectWS = useCallback(() => {
    wsRef.current?.close();
    onStatusChange('disconnected');
  }, [onStatusChange]);

  // ── Frame loop ─────────────────────────────────────────────────────────────
  const sendFrame = useCallback(() => {
    if (!webcamRef.current || wsRef.current?.readyState !== WebSocket.OPEN) return;
    const img = webcamRef.current.getScreenshot({ width: 320, height: 240 });
    if (!img) return;
    wsRef.current.send(JSON.stringify({ frame: img }));
  }, []);

  useEffect(() => {
    if (active) {
      connectWS();
      timerRef.current = setInterval(sendFrame, 1000 / FPS);
    } else {
      clearInterval(timerRef.current);
      disconnectWS();
    }
    return () => clearInterval(timerRef.current);
  }, [active, connectWS, disconnectWS, sendFrame]);

  // cleanup on unmount
  useEffect(() => () => { clearInterval(timerRef.current); wsRef.current?.close(); }, []);

  return (
    <div className="camera-wrapper">
      <div className="webcam-container">
        {camError ? (
          <div className="cam-error">
            <span>📷</span>
            <p>Camera access denied.</p>
            <small>{camError}</small>
          </div>
        ) : (
          <Webcam
            ref={webcamRef}
            audio={false}
            screenshotFormat="image/jpeg"
            screenshotQuality={0.7}
            mirrored={mirror}
            videoConstraints={{ width: 640, height: 480, facingMode: 'user' }}
            onUserMediaError={(e) => setCamError(e.message || 'Unknown error')}
            className="webcam-feed"
          />
        )}
        {active && <div className="rec-indicator">⬤ LIVE</div>}
      </div>

      <div className="camera-controls">
        <button
          className={`btn ${active ? 'btn-danger' : 'btn-primary'}`}
          onClick={() => setActive(v => !v)}
        >
          {active ? '⏹ Stop' : '▶ Start Detecting'}
        </button>

        <button
          className="btn btn-secondary"
          onClick={() => setMirror(v => !v)}
          title="Flip camera"
        >
          ↔ Mirror
        </button>
      </div>

      <p className="cam-hint">
        {active
          ? '🟢 Detecting — show your hand sign clearly in the frame'
          : '⚪ Press "Start Detecting" to begin'}
      </p>
    </div>
  );
}
