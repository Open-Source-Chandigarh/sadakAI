import React, { useState, useRef, useEffect } from 'react';
import { Send, Bot, User, Menu } from 'lucide-react';

const MobileChatbot = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Hello! I'm an AI assistant. How can I help you today?",
      sender: 'ai'
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isMenuOpen, setIsMenuOpen] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: inputMessage })
      });
      const data = await response.json();

      // Add AI response to messages
      if (data.status === 'success') {
        setMessages(prevMessages => [
          ...prevMessages,
          { id: Date.now(), text: data.message, sender: 'ai' }
        ]);
      }
    } catch (error) {
      console.error('Error sending message:', error);
    }
  };

  return (
    <div className="flex flex-col h-screen bg-gray-900 text-white">
      {/* Mobile Header */}
      <div className="p-4 bg-gray-800 flex justify-between items-center">
        <div className="flex items-center">
          <Bot className="mr-2 text-blue-400" />
          <h1 className="text-xl font-bold">AI Chatbot</h1>
        </div>
        <button
          onClick={() => setIsMenuOpen(!isMenuOpen)}
          className="p-2 rounded-md hover:bg-gray-700"
        >
          <Menu className="text-white" />
        </button>
      </div>

      {/* Side Menu (for mobile) */}
      {isMenuOpen && (
        <div className="absolute right-0 top-16 w-64 bg-gray-800 z-10 rounded-lg shadow-lg">
          <div className="p-4">
            <h2 className="text-lg font-semibold mb-2">Menu</h2>
            <ul className="space-y-2">
              <li className="p-2 hover:bg-gray-700 rounded">New Chat</li>
              <li className="p-2 hover:bg-gray-700 rounded">Settings</li>
              <li className="p-2 hover:bg-gray-700 rounded">Help</li>
            </ul>
          </div>
        </div>
      )}

      {/* Messages Container */}
      <div className="flex-grow overflow-y-auto p-4 space-y-4">
        {messages.map((message) => (
          <div
            key={message.id}
            className={`flex items-start space-x-2 ${message.sender === 'ai' ? 'justify-start' : 'justify-end'
              }`}
          >
            {message.sender === 'ai' && (
              <Bot className="w-6 h-6 text-blue-400" />
            )}
            <div
              className={`
                max-w-[80%] px-3 py-2 rounded-lg text-sm
                ${message.sender === 'ai'
                  ? 'bg-gray-700 text-white'
                  : 'bg-blue-600 text-white'
                }
              `}
            >
              {message.text}
            </div>
            {message.sender === 'user' && (
              <User className="w-6 h-6 text-gray-400" />
            )}
          </div>
        ))}
        <div ref={messagesEndRef} />
      </div>

      {/* Input Area */}
      <div className="p-3 bg-gray-800 flex items-center">
        <input
          type="text"
          value={inputMessage}
          onChange={(e) => setInputMessage(e.target.value)}
          onKeyPress={(e) => e.key === 'Enter' && handleSendMessage()}
          placeholder="Type your message..."
          className="
            flex-grow 
            bg-gray-700 
            text-white 
            p-2 
            rounded-l-lg 
            text-sm
            focus:outline-none 
            focus:ring-2 
            focus:ring-blue-500
          "
        />
        <button
          onClick={handleSendMessage}
          className="
            bg-blue-600 
            text-white 
            p-2 
            rounded-r-lg 
            hover:bg-blue-700 
            transition-colors
            flex 
            items-center 
            justify-center
          "
        >
          <Send className="w-4 h-4" />
        </button>
      </div>
    </div>
  );
};

export default MobileChatbot;
