import React, { useState, useRef, useEffect } from 'react';
import ReactMarkdown from 'react-markdown';
import { Send, Bot, User, MessageCircle, HelpCircle, github } from 'lucide-react';

const DesktopChatbot = () => {
  const [messages, setMessages] = useState([
    {
      id: 1,
      text: "Hello! Welcome to sadak-ai! How can I help you today?",
      sender: 'ai'
    }
  ]);
  const [inputMessage, setInputMessage] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [isHelpModalOpen, setIsHelpModalOpen] = useState(false);
  const messagesEndRef = useRef(null);

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: "smooth" });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (inputMessage.trim() === '') return;

    // Add user message immediately
    const userMessage = {
      id: Date.now(),
      text: inputMessage,
      sender: 'user'
    };

    setMessages(prevMessages => [...prevMessages, userMessage]);
    setInputMessage('');
    setIsLoading(true);

    try {
      const response = await fetch('/api/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ message: inputMessage })
      });

      const data = await response.json();

      if (data.status === 'success') {
        const aiMessage = {
          id: Date.now(),
          text: data.response,
          sender: 'ai'
        };

        setMessages(prevMessages => [...prevMessages, aiMessage]);
      } else {
        // Handle error scenario
        const errorMessage = {
          id: Date.now(),
          text: "Sorry, there was an error processing your message.",
          sender: 'ai'
        };

        setMessages(prevMessages => [...prevMessages, errorMessage]);
      }
    } catch (error) {
      console.error('Error sending message:', error);

      const errorMessage = {
        id: Date.now(),
        text: "Network error. Please try again.",
        sender: 'ai'
      };

      setMessages(prevMessages => [...prevMessages, errorMessage]);
    } finally {
      setIsLoading(false);
    }
  };

  const handleNewChat = () => {
    // Reset to initial welcome message
    setMessages([
      {
        id: 1,
        text: "Hello! Welcome to sadak-ai! How can I help you today?",
        sender: 'ai'
      }
    ]);
  };

  const HelpModal = () => {
    if (!isHelpModalOpen) return null;

    return (
      <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
        <div className="bg-gray-800 p-6 rounded-lg max-w-md w-full">
          <h2 className="text-2xl font-bold mb-4 text-white">Help</h2>
          <p className="text-gray-300 mb-4">
            Welcome to sadakAI!<br></br>
            Ask sadakAI anything related to learning a new technologies, asking for refrences, or any other queries you have. (currently the dataset is small, only limited to basic queries related to frontend, backend, androind and ai-ds)
          </p>
          <button
            onClick={() => setIsHelpModalOpen(false)}
            className="bg-blue-600 text-white px-4 py-2 rounded hover:bg-blue-700"
          >
            Close
          </button>
        </div>
      </div>
    );
  };

  return (
    <>
      <HelpModal />
      <div className="flex h-screen bg-gray-900 text-white overflow-hidden">
        {/* Sidebar - Fixed width and scrollable if content overflows */}
        <div className="w-64 bg-gray-800 p-4 border-r border-gray-700 overflow-y-auto flex-shrink-0 flex flex-col">
          <div className="flex-grow">
            <div className="flex items-center mb-6">
              <Bot className="mr-2 text-blue-400 w-8 h-8" />
              <h1 className="text-2xl font-bold">sadak-AI</h1>
            </div>

            <nav className="space-y-2">
              <div
                onClick={handleNewChat}
                className="flex items-center p-2 hover:bg-gray-700 rounded cursor-pointer"
              >
                <MessageCircle className="mr-2 text-blue-400" />
                <span>New Chat</span>
              </div>
              <div
                onClick={() => setIsHelpModalOpen(true)}
                className="flex items-center p-2 hover:bg-gray-700 rounded cursor-pointer"
              >
                <HelpCircle className="mr-2 text-gray-400" />
                <span>Help</span>
              </div>
            </nav>
          </div>

          {/* GitHub Link at the bottom */}
          <a
            href="https://github.com/Open-Source-Chandigarh/sadakAI"
            target="_blank"
            rel="noopener noreferrer"
            className="flex items-center p-2 hover:bg-gray-700 rounded cursor-pointer mt-4"
          >
            <github className="mr-2 text-gray-400" />
            <span>Visit GitHub</span>
          </a>
        </div>

        {/* Main Chat Area */}
        <div className="flex flex-col flex-grow overflow-hidden">
          {/* Messages Container */}
          <div className="flex-grow overflow-y-auto p-6 space-y-4">
            {messages.map((message) => (
              <div
                key={message.id}
                className={`flex items-start space-x-3 ${message.sender === 'ai' ? 'justify-start' : 'justify-end'
                  }`}
              >
                {message.sender === 'ai' && (
                  <Bot className="w-8 h-8 text-blue-400 flex-shrink-0" />
                )}
                <div
                  className={`
                    max-w-[60%] px-4 py-2 rounded-lg 
                    ${message.sender === 'ai'
                      ? 'bg-gray-700 text-white'
                      : 'bg-blue-600 text-white'
                    }
                    prose prose-invert max-w-full
                  `}
                >
                  <ReactMarkdown>{message.text}</ReactMarkdown>
                </div>
                {message.sender === 'user' && (
                  <User className="w-8 h-8 text-gray-400 flex-shrink-0" />
                )}
              </div>
            ))}
            {isLoading && (
              <div className="flex justify-start items-center space-x-3">
                <Bot className="w-8 h-8 text-blue-400" />
                <div className="bg-gray-700 px-4 py-2 rounded-lg">
                  Typing...
                </div>
              </div>
            )}
            <div ref={messagesEndRef} />
          </div>

          {/* Input Area */}
          <div className="p-4 bg-gray-800 flex items-center">
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
                p-3 
                rounded-l-lg 
                focus:outline-none 
                focus:ring-2 
                focus:ring-blue-500
              "
              disabled={isLoading}
            />
            <button
              onClick={handleSendMessage}
              disabled={isLoading}
              className="
                bg-blue-600 
                text-white 
                p-3 
                rounded-r-lg 
                hover:bg-blue-700 
                transition-colors
                flex 
                items-center 
                justify-center
                disabled:opacity-50
                disabled:cursor-not-allowed
              "
            >
              <Send className="w-6 h-6" />
            </button>
          </div>
        </div>
      </div>
    </>
  );
};

export default DesktopChatbot;