import React, { useContext } from 'react'
import { BrowserRouter as Router, Routes, Route, Navigate } from 'react-router-dom'
import { Toaster } from 'sonner'
import './App.css'
import { AuthProvider, AuthContext } from './context/AuthContext'

// Pages
import Dashboard from './pages/Dashboard'
import Artists from './pages/Artists'
import Channels from './pages/Channels'
import News from './pages/News'
import Accounts from './pages/Accounts'
import Boards from './pages/Boards'
import Settings from './pages/Settings'
import Login from './pages/Login'
import Signup from './pages/Signup'
import SearchArtistPage from './pages/SearchArtistPage' // New import

// Components
import Sidebar from './components/Sidebar'
import Header from './components/Header'
import Footer from './components/Footer'

const AppContent: React.FC = () => {
  const authContext = useContext(AuthContext);

  if (!authContext) {
    throw new Error('AuthContext must be used within an AuthProvider');
  }

  const { isAuthenticated } = authContext;

  return (
    <div className="min-h-screen bg-gradient-to-br from-slate-900 via-purple-900 to-slate-900 flex flex-col">
      <div className="flex-1 flex">
        {isAuthenticated ? (
          <>
            <Sidebar />
            <div className="flex-1 flex flex-col">
              <Header />
              <main className="flex-1 p-6">
                <Routes>
                  <Route path="/" element={<Dashboard />} />
                  <Route path="/artists" element={<Artists />} />
                  <Route path="/search-artist" element={<SearchArtistPage />} /> {/* New Route */}
                  <Route path="/channels" element={<Channels />} />
                  <Route path="/news" element={<News />} />
                  <Route path="/accounts" element={<Accounts />} />
                  <Route path="/boards" element={<Boards />} />
                  <Route path="/settings" element={<Settings />} />
                  <Route path="*" element={<Navigate to="/" replace />} />
                </Routes>
              </main>
            </div>
          </>
        ) : (
          <div className="flex-1 flex flex-col">
            <Routes>
              <Route path="/login" element={<Login />} />
              <Route path="/signup" element={<Signup />} />
              <Route path="*" element={<Navigate to="/login" replace />} />
            </Routes>
          </div>
        )}
      </div>
      <Footer />
      <Toaster position="top-right" richColors />
    </div>
  );
};

function App() {
  return (
    <Router>
      <AuthProvider>
        <AppContent />
      </AuthProvider>
    </Router>
  );
}

export default App
