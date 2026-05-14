import React from 'react';
import { Search, Bell, Moon, User } from 'lucide-react';

const TopBar = () => {
  return (
    <div className="top-bar glass">
      <div className="search-container">
        <Search size={18} className="search-icon" />
        <input type="text" placeholder="Search media, radio, streams..." className="search-input" />
      </div>

      <div className="top-bar-actions">
        <button className="icon-btn"><Bell size={20} /></button>
        <button className="icon-btn"><Moon size={20} /></button>
        <div className="user-profile">
          <User size={20} />
        </div>
      </div>
    </div>
  );
};

export default TopBar;
