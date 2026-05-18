import React, { useState, useRef, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';

const API_BASE = process.env.REACT_APP_API_URL || 'http://localhost:8000';

const QUICK_WORDS = [
  'hello', 'yes', 'no', 'please', 'thankyou',
  'sorry', 'help', 'good', 'iloveyou', 'stop',
];

export default function SentenceBuilder({ sentence, onClear, onRemoveLast, onAddWord }) {
  const [mode, setMode]         = useState('words');   // 'words' | 'sentence'
  const [ttsLoading, setTts]    = useState(false);
  const [ttsError, setTtsError] = useState('');
  const audioRef                = useRef(null);

  // ── Build display text ─────────────────────────────────────────────────────
  const displayText = sentence.join(mode === 'sentence' ? ' ' : ' + ');
  const speakText   = sentence.join(' ');

  // ── Text-to-Speech ─────────────────────────────────────────────────────────
  const speak = useCallback(async () => {
    if (!speakText.trim()) return;
    setTts(true);
    setTtsError('');
    try {
      const res = await fetch(`${API_BASE}/api/tts`, {
        method:  'POST',
        headers: { 'Content-Type': 'application/json' },
        body:    JSON.stringify({ text: speakText }),
      });
      if (!res.ok) throw new Error(`TTS error ${res.status}`);
      const blob = await res.blob();
      const url  = URL.createObjectURL(blob);
      if (audioRef.current) {
        audioRef.current.src = url;
        audioRef.current.play();
      }
    } catch (e) {
      setTtsError(e.message);
      // fallback to browser TTS
      if ('speechSynthesis' in window) {
        const utt = new SpeechSynthesisUtterance(speakText);
        window.speechSynthesis.speak(utt);
      }
    } finally {
      setTts(false);
    }
  }, [speakText]);

  // ── Copy ───────────────────────────────────────────────────────────────────
  const copyText = () => {
    navigator.clipboard.writeText(speakText).catch(() => {});
  };

  return (
    <div className="sentence-builder">
      <audio ref={audioRef} hidden />

      {/* Header */}
      <div className="sb-header">
        <h2 className="panel-title">💬 Sentence Builder</h2>
        <div className="mode-toggle">
          {['words', 'sentence'].map(m => (
            <button
              key={m}
              className={`mode-btn ${mode === m ? 'active' : ''}`}
              onClick={() => setMode(m)}
            >
              {m === 'words' ? '🔤 Words' : '📝 Sentence'}
            </button>
          ))}
        </div>
      </div>

      {/* Word chips */}
      <div className="word-chips" aria-label="Built sentence">
        <AnimatePresence>
          {sentence.length === 0 ? (
            <motion.p
              className="chips-placeholder"
              initial={{ opacity: 0 }}
              animate={{ opacity: 1 }}
            >
              Detected signs will appear here…
            </motion.p>
          ) : (
            sentence.map((word, i) => (
              <motion.span
                key={`${word}-${i}`}
                className="chip"
                initial={{ scale: 0, opacity: 0 }}
                animate={{ scale: 1, opacity: 1 }}
                exit={{   scale: 0, opacity: 0 }}
                transition={{ type: 'spring', stiffness: 400, damping: 25 }}
                onClick={() => {
                  // click chip to remove it
                  const next = sentence.filter((_, idx) => idx !== i);
                  onClear();
                  next.forEach(w => onAddWord(w));
                }}
                title="Click to remove"
              >
                {word}
              </motion.span>
            ))
          )}
        </AnimatePresence>
      </div>

      {/* Full sentence display (sentence mode) */}
      {mode === 'sentence' && sentence.length > 0 && (
        <div className="sentence-text">
          <span>{speakText}</span>
        </div>
      )}

      {/* Controls */}
      <div className="sb-controls">
        <button
          className="btn btn-primary btn-tts"
          onClick={speak}
          disabled={ttsLoading || sentence.length === 0}
        >
          {ttsLoading ? '⏳' : '🔊'} Speak
        </button>
        <button
          className="btn btn-secondary"
          onClick={copyText}
          disabled={sentence.length === 0}
        >
          📋 Copy
        </button>
        <button
          className="btn btn-secondary"
          onClick={onRemoveLast}
          disabled={sentence.length === 0}
        >
          ⌫ Undo
        </button>
        <button
          className="btn btn-danger"
          onClick={onClear}
          disabled={sentence.length === 0}
        >
          🗑 Clear
        </button>
      </div>

      {ttsError && (
        <p className="tts-error">⚠ TTS error — using browser fallback</p>
      )}

      {/* Quick-add buttons */}
      <div className="quick-add">
        <p className="quick-title">Quick Add:</p>
        <div className="quick-btns">
          {QUICK_WORDS.map(w => (
            <button key={w} className="quick-btn" onClick={() => onAddWord(w)}>
              {w}
            </button>
          ))}
        </div>
      </div>
    </div>
  );
}
