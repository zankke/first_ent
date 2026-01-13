import React, { useContext } from 'react'
import { Link, useLocation } from 'react-router-dom'
import { 
  LayoutDashboard, 
  Users, 
  Radio, 
  UserCheck, 
  MessageSquare, 
  Settings,
  Sparkles,
  Newspaper,
  LogIn, LogOut
} from 'lucide-react'
import { AuthContext } from '../context/AuthContext'

const Sidebar = () => {
  const location = useLocation()
  const authContext = useContext(AuthContext);

  if (!authContext) {
    throw new Error('AuthContext must be used within an AuthProvider');
  }

  const { user, account, level, logout } = authContext;
  
  const menuItems = [
    { path: '/', icon: LayoutDashboard, label: 'Dashboard' },
    { path: '/artists', icon: Users, label: '아티스트 관리' },
    { path: '/news', icon: Newspaper, label: '뉴스 모니터링' },
    { path: '/channels', icon: Radio, label: '채널 관리' },
    { path: '/accounts', icon: UserCheck, label: '계정 관리' },
    { path: '/boards', icon: MessageSquare, label: '게시판 관리' },
    { path: '/settings', icon: Settings, label: '설정' },
  ]

  return (
    <div className="w-64 bg-gray-800 rounded-r-2xl p-6 h-screen relative z-50">
      <Link to="/" className="flex items-center space-x-3 mb-8 cursor-pointer">
        <div className="w-10 h-10 bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl flex items-center justify-center">
          <Sparkles className="w-6 h-6 text-white" />
        </div>
        <div>
          <h1 className="text-xl font-bold text-white">First Ent</h1>
          <p className="text-sm text-gray-400">Artist Management</p>
        </div>
      </Link>
      
      <nav className="space-y-2">
        {menuItems.map((item) => {
          const Icon = item.icon
          const isActive = location.pathname === item.path
          
          return (
            <Link
              key={item.path}
              to={item.path}
              className={`flex items-center space-x-3 px-4 py-3 rounded-xl transition-all duration-200 group ${
                isActive
                  ? 'bg-gray-700 text-white shadow-lg'
                  : 'text-white hover:bg-gray-700'
              }`}
            >
              <Icon className={`w-5 h-5 ${isActive ? 'text-white' : 'text-gray-400 group-hover:text-white'}`} />
              <span className="font-medium">{item.label}</span>
            </Link>
          )
        })}
      </nav>
      
      <div className="absolute bottom-6 left-6 right-6">
        <div className="bg-gray-700 rounded-xl p-4">
          {user ? (
            <div className="flex items-center space-x-3">
              <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-500 rounded-full flex items-center justify-center">
                <span className="text-sm font-bold text-white">{(user.email || 'U').charAt(0).toUpperCase()}</span>
              </div>
              <div className="flex-1">
                <p className="text-sm font-medium text-white">{user.email || 'User'}</p>
                {level ? (
                  <p className="text-xs text-gray-400">
                    {level === 'admin' ? '관리자' : 
                     level === 'manager' ? '매니저' : '뷰어'}
                    {account && ` • ${account.uid}`}
                  </p>
                ) : (
                  <p className="text-xs text-gray-400">권한 없음</p>
                )}
              </div>
              <button onClick={async () => await logout()} className="ml-auto p-2 rounded-full hover:bg-gray-600 transition-colors">
                <LogOut className="w-5 h-5 text-white" />
              </button>
            </div>
          ) : (
            <Link to="/login" className="flex items-center space-x-3 px-4 py-2 rounded-xl bg-primary text-primary-foreground hover:bg-primary/90 transition-colors w-full justify-center">
              <LogIn className="w-5 h-5" />
              <span>로그인</span>
            </Link>
          )}
        </div>
      </div>
    </div>
  )
}

export default Sidebar
