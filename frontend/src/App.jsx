import React, { useState, useCallback } from 'react';
import { motion, AnimatePresence } from 'framer-motion';
import Camera from './components/Camera';
import SignDisplay from './components/SignDisplay';
import SentenceBuilder from './components/SentenceBuilder';
import SignList from './components/SignList';
import Header from './components/Header';
import StatusBar from './components/StatusBar';
import './styles/App.css';

export default function App() {
  const [currentSign, setCurrentSign]       = useState(null);
  const [confidence, setConfidence]         = useState(0);
  const [top5, setTop5]                     = useState([]);
  const [sentence, setSentence]             = useState([]);
  const [wsStatus, setWsStatus]             = useState('disconnected'); // connected | disconnected | error
  const [handDetected, setHandDetected]     = useState(false);
  const [activeTab, setActiveTab]           = useState('translator');  // translator | signs

  // Called by Camera when WS sends a prediction
  const handlePrediction = useCallback((data) => {
    if (data.type === 'prediction') {
      setCurrentSign(data.sign);
      setConfidence(data.confidence);
      setTop5(data.top5 || []);
      // Auto-add to sentence builder
      setSentence(prev => {
        const last = prev[prev.length - 1];
        if (last === data.sign) return prev;   // debounce duplicates
        return [...prev, data.sign];
      });
    }
    if (data.hand_detected !== undefined) setHandDetected(data.hand_detected);
  }, []);

  const clearSentence  = useCallback(() => setSentence([]),   []);
  const removeLastWord = useCallback(() => setSentence(p => p.slice(0, -1)), []);
  const addWord        = useCallback((w) => setSentence(p => [...p, w]),     []);

  return (
    <div className="app">
      <Header />
      <StatusBar wsStatus={wsStatus} handDetected={handDetected} />

      {/* Tab nav */}
      <nav className="tab-nav">
        {['translator', 'signs'].map(tab => (
          <button
            key={tab}
            className={`tab-btn ${activeTab === tab ? 'active' : ''}`}
            onClick={() => setActiveTab(tab)}
          >
            {tab === 'translator' ? '🤟 Translator' : '📖 Sign List'}
          </button>
        ))}
      </nav>

      <AnimatePresence mode="wait">
        {activeTab === 'translator' ? (
          <motion.div
            key="translator"
            className="main-grid"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.25 }}
          >
            {/* Left — camera */}
            <section className="panel camera-panel">
              <h2 className="panel-title">📷 Live Feed</h2>
              <Camera
                onPrediction={handlePrediction}
                onStatusChange={setWsStatus}
              />
            </section>

            {/* Right — results */}
            <section className="panel results-panel">
              <SignDisplay
                sign={currentSign}
                confidence={confidence}
                top5={top5}
              />
              <SentenceBuilder
                sentence={sentence}
                onClear={clearSentence}
                onRemoveLast={removeLastWord}
                onAddWord={addWord}
              />
            </section>
          </motion.div>
        ) : (
          <motion.div
            key="signs"
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            exit={{ opacity: 0, y: -10 }}
            transition={{ duration: 0.25 }}
          >
            <SignList />
          </motion.div>
        )}
      </AnimatePresence>
    </div>
  );
}
