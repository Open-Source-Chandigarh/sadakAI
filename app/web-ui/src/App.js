import React, { useState, useEffect } from 'react';
import MobileChatbot from './components/mobileView';
import DesktopChatbot from './components/desktopView';
import './index.css';

function App() {
  const [isMobile, setIsMobile] = useState(window.innerWidth < 768);

  useEffect(() => {
    const handleResize = () => {
      setIsMobile(window.innerWidth < 768);
    };

    window.addEventListener('resize', handleResize);
    return () => window.removeEventListener('resize', handleResize);
  }, []);

  return isMobile ? <MobileChatbot /> : <DesktopChatbot />;
}

export default App;
