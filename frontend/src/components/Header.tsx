import React, { useState, useContext } from 'react'
import { useNavigate } from 'react-router-dom'
import { Bell, Search, User, LogOut } from 'lucide-react'
import { AuthContext } from '../context/AuthContext'

const Header = () => {
  const [searchQuery, setSearchQuery] = useState('')
  const navigate = useNavigate()
  const authContext = useContext(AuthContext);

  if (!authContext) {
    throw new Error('AuthContext must be used within an AuthProvider');
  }

  const { logout } = authContext;

  const handleSearch = () => {
    if (searchQuery.trim()) {
      navigate(`/artists?query=${searchQuery.trim()}`)
    }
  }

  const handleLogout = async () => {
    await logout();
    navigate('/login');
  };

  return (
    <header className="glass rounded-2xl m-6 mb-0 p-4">
      <div className="flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <h2 className="text-2xl font-bold gradient-text">[TAMS_v1.0] Artist Management System v1.0</h2>
        </div>
        
        <div className="flex items-center space-x-4">
          <div className="relative">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-4 h-4" />
            <input
              type="text"
              placeholder="검색..."
              className="pl-10 pr-4 py-2 bg-muted/50 border border-border rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/50 text-sm"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyPress={(e) => {
                if (e.key === 'Enter') {
                  handleSearch()
                }
              }}
            />
          </div>
          
          <button className="relative p-2 text-muted-foreground hover:text-foreground transition-colors">
            <Bell className="w-5 h-5" />
            <span className="absolute -top-1 -right-1 w-3 h-3 bg-red-500 rounded-full text-xs flex items-center justify-center text-white">
              3
            </span>
          </button>
          
          <div className="flex items-center space-x-2 p-2 rounded-xl hover:bg-muted/50 transition-colors cursor-pointer">
            <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center">
              <User className="w-4 h-4 text-white" />
            </div>
            <div className="flex flex-col">
              <span className="text-sm font-medium">{authContext.user?.email || 'User'}</span>
              {authContext.level && (
                <span className="text-xs text-muted-foreground">
                  {authContext.level === 'admin' ? '관리자' : 
                   authContext.level === 'manager' ? '매니저' : '뷰어'}
                </span>
              )}
            </div>
          </div>
          <button
            onClick={handleLogout}
            className="flex items-center space-x-2 p-2 rounded-xl hover:bg-muted/50 transition-colors cursor-pointer"
          >
            <LogOut className="w-5 h-5 text-muted-foreground" />
            <span className="text-sm font-medium">Logout</span>
          </button>
        </div>
      </div>
    </header>
  )
}

export default Header
