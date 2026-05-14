import React from 'react';
import { motion } from 'framer-motion';
import { Play, TrendingUp, Radio, Headphones } from 'lucide-react';

const QuickAction = ({ icon: Icon, label, gradient }) => (
  <motion.div
    whileHover={{ scale: 1.05 }}
    className="quick-action-card"
    style={{ background: gradient }}
  >
    <Icon size={32} color="white" />
    <span className="quick-action-label">{label}</span>
  </motion.div>
);

const Dashboard = () => {
  return (
    <div className="view-container">
      <div className="hero-banner glass">
        <div className="hero-content">
          <h2 className="hero-title">Nexus Cinematic</h2>
          <p className="hero-subtitle">The most advanced multimedia platform on the web.</p>
          <button className="primary-btn">Start Watching</button>
        </div>
      </div>

      <div className="section">
        <h3 className="section-title">Quick Actions</h3>
        <div className="quick-actions-grid">
          <QuickAction icon={Play} label="Cinema Player" gradient="linear-gradient(135deg, #1e1e3f, #8A2BE2)" />
          <QuickAction icon={TrendingUp} label="Audio Mixer" gradient="linear-gradient(135deg, #0d1a1a, #00C853)" />
          <QuickAction icon={Radio} label="Live Radio" gradient="linear-gradient(135deg, #1a0d0d, #FF4444)" />
          <QuickAction icon={Headphones} label="Studio Library" gradient="linear-gradient(135deg, #0d1a2b, #00E5FF)" />
        </div>
      </div>

      <div className="section">
        <h3 className="section-title">Recently Played</h3>
        <div className="recent-grid">
          {[1, 2, 3].map((i) => (
            <div key={i} className="recent-card glass glass-hover">
              <div className="recent-thumb" />
              <div className="recent-info">
                <span className="recent-title">Cinematic Video {i}</span>
                <span className="recent-meta">Resumed at 12:45</span>
              </div>
            </div>
          ))}
        </div>
      </div>
    </div>
  );
};

export default Dashboard;
