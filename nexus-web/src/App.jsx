import React, { useState } from 'react';
import Sidebar from './components/Sidebar';
import TopBar from './components/TopBar';
import Dashboard from './views/Dashboard';
import { motion, AnimatePresence } from 'framer-motion';

function App() {
  const [activeTab, setActiveTab] = useState(0);

  const renderContent = () => {
    switch (activeTab) {
      case 0: return <Dashboard />;
      default: return (
        <div className="view-container">
          <div className="glass p-20 text-center">
            <h2 className="text-4xl font-black mb-4">Under Construction</h2>
            <p className="text-gray-400">This feature is coming soon to the Nexus Web Suite.</p>
          </div>
        </div>
      );
    }
  };

  return (
    <div className="app-shell">
      <Sidebar activeTab={activeTab} setActiveTab={setActiveTab} />
      <main className="main-content">
        <TopBar />
        <AnimatePresence mode="wait">
          <motion.div
            key={activeTab}
            initial={{ opacity: 0, x: 20 }}
            animate={{ opacity: 1, x: 0 }}
            exit={{ opacity: 0, x: -20 }}
            transition={{ duration: 0.3 }}
          >
            {renderContent()}
          </motion.div>
        </AnimatePresence>
      </main>
    </div>
  );
}

export default App;
