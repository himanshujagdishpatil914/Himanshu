import React from 'react';
import { motion, AnimatePresence } from 'framer-motion';

export default function SignDisplay({ sign, confidence, top5 }) {
  return (
    <div className="sign-display">
      <h2 className="panel-title">🔤 Detected Sign</h2>

      <AnimatePresence mode="wait">
        {sign ? (
          <motion.div
            key={sign}
            className="sign-card"
            initial={{ scale: 0.7, opacity: 0 }}
            animate={{ scale: 1,   opacity: 1 }}
            exit={{   scale: 1.1,  opacity: 0 }}
            transition={{ type: 'spring', stiffness: 300, damping: 20 }}
          >
            <span className="sign-label">{sign}</span>
            <div className="conf-row">
              <div className="conf-bar-track">
                <motion.div
                  className="conf-bar-fill"
                  initial={{ width: 0 }}
                  animate={{ width: `${confidence}%` }}
                  transition={{ duration: 0.4 }}
                  style={{
                    background: confidence > 90
                      ? '#22c55e'
                      : confidence > 75
                      ? '#f59e0b'
                      : '#ef4444',
                  }}
                />
              </div>
              <span className="conf-value">{confidence}%</span>
            </div>
          </motion.div>
        ) : (
          <motion.div
            key="placeholder"
            className="sign-placeholder"
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
          >
            <span>🤲</span>
            <p>Show a sign to the camera</p>
          </motion.div>
        )}
      </AnimatePresence>

      {/* Top-5 predictions */}
      {top5.length > 0 && (
        <div className="top5">
          <h3 className="top5-title">Top Predictions</h3>
          {top5.map((item, i) => (
            <div key={item.sign} className="top5-row">
              <span className="top5-rank">#{i + 1}</span>
              <span className="top5-sign">{item.sign}</span>
              <div className="top5-bar-track">
                <div
                  className="top5-bar-fill"
                  style={{ width: `${item.prob}%`, opacity: 1 - i * 0.15 }}
                />
              </div>
              <span className="top5-prob">{item.prob}%</span>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
