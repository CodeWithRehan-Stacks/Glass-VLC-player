
import React from 'react';
import { motion } from 'framer-motion';
import { LayoutDashboard, Play, Activity, Radio, Library, History, Settings } from 'lucide-react';

const SidebarItem = ({ icon: Icon, label, active, onClick }) => (
  <motion.div
    whileHover={{ x: 5 }}
    onClick={onClick}
    className={`sidebar-item ${active ? 'active' : ''}`}
  >
    <Icon size={20} />
    <span className="sidebar-label">{label}</span>
  </motion.div>
);

const Sidebar = ({ activeTab, setActiveTab }) => {
  const menuItems = [
    { id: 0, label: 'Dashboard', icon: LayoutDashboard },
    { id: 1, label: 'Cinema', icon: Play },
    { id: 2, label: 'Mixer', icon: Activity },
    { id: 3, label: 'Radio', icon: Radio },
    { id: 4, label: 'Library', icon: Library },
    { id: 5, label: 'History', icon: History },
  ];

  return (
    <div className="sidebar glass">
      <div className="sidebar-logo">
        <h1 className="logo-text">NEXUS</h1>
        <span className="logo-subtext">Studio Web</span>
      </div>

      <nav className="sidebar-nav">
        {menuItems.map((item) => (
          <SidebarItem
            key={item.id}
            {...item}
            active={activeTab === item.id}
            onClick={() => setActiveTab(item.id)}
          />
        ))}
      </nav>

      <div className="sidebar-footer">
        <SidebarItem icon={Settings} label="Settings" onClick={() => setActiveTab(6)} active={activeTab === 6} />
      </div>
    </div>
  );
};

export default Sidebar;

