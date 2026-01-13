import React, { useState } from 'react'
import { Save, Key, Database, Bell, Shield, Globe } from 'lucide-react'

const Settings = () => {
  const [activeTab, setActiveTab] = useState('api')

  const tabs = [
    { id: 'api', label: 'API 설정', icon: Key },
    { id: 'database', label: '데이터베이스', icon: Database },
    { id: 'notifications', label: '알림 설정', icon: Bell },
    { id: 'security', label: '보안', icon: Shield },
    { id: 'general', label: '일반', icon: Globe }
  ]

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold gradient-text mb-2">설정</h1>
        <p className="text-muted-foreground">시스템 설정을 관리하세요</p>
      </div>
      
      <div className="grid grid-cols-1 lg:grid-cols-4 gap-6">
        {/* 탭 네비게이션 */}
        <div className="glass rounded-2xl p-6">
          <nav className="space-y-2">
            {tabs.map((tab) => {
              const Icon = tab.icon
              return (
                <button
                  key={tab.id}
                  onClick={() => setActiveTab(tab.id)}
                  className={`w-full flex items-center space-x-3 px-4 py-3 rounded-xl transition-all duration-200 ${
                    activeTab === tab.id
                      ? 'bg-primary text-primary-foreground shadow-lg'
                      : 'text-muted-foreground hover:text-foreground hover:bg-muted/50'
                  }`}
                >
                  <Icon className="w-5 h-5" />
                  <span className="font-medium">{tab.label}</span>
                </button>
              )
            })}
          </nav>
        </div>
        
        {/* 설정 내용 */}
        <div className="lg:col-span-3">
          <div className="glass rounded-2xl p-6">
            {activeTab === 'api' && (
              <div className="space-y-6">
                <div>
                  <h2 className="text-xl font-semibold mb-2">API 키 관리</h2>
                  <p className="text-muted-foreground">소셜미디어 API 키를 관리하세요</p>
                </div>
                
                <div className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <label className="text-sm font-medium">Instagram API Key</label>
                      <input
                        type="password"
                        placeholder="Instagram API 키를 입력하세요"
                        className="w-full px-3 py-2 bg-muted/50 border border-border rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/50"
                      />
                    </div>
                    <div className="space-y-2">
                      <label className="text-sm font-medium">YouTube API Key</label>
                      <input
                        type="password"
                        placeholder="YouTube API 키를 입력하세요"
                        className="w-full px-3 py-2 bg-muted/50 border border-border rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/50"
                      />
                    </div>
                    <div className="space-y-2">
                      <label className="text-sm font-medium">TikTok API Key</label>
                      <input
                        type="password"
                        placeholder="TikTok API 키를 입력하세요"
                        className="w-full px-3 py-2 bg-muted/50 border border-border rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/50"
                      />
                    </div>
                    <div className="space-y-2">
                      <label className="text-sm font-medium">SERP API Key</label>
                      <input
                        type="password"
                        placeholder="SERP API 키를 입력하세요"
                        className="w-full px-3 py-2 bg-muted/50 border border-border rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/50"
                      />
                    </div>
                    <div className="space-y-2">
                      <label className="text-sm font-medium">Perplexity API Key</label>
                      <input
                        type="password"
                        placeholder="Perplexity API 키를 입력하세요"
                        className="w-full px-3 py-2 bg-muted/50 border border-border rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/50"
                      />
                    </div>
                  <div className="space-y-2">
                    <label className="text-sm font-medium">OpenAI API Key</label>
                    <input
                      type="password"
                      placeholder="OpenAI API 키를 입력하세요"
                      className="w-full px-3 py-2 bg-muted/50 border border-border rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/50"
                    />
                  </div>
                  </div>
                </div>
              </div>
            )}
            
            {activeTab === 'database' && (
              <div className="space-y-6">
                <div>
                  <h2 className="text-xl font-semibold mb-2">데이터베이스 설정</h2>
                  <p className="text-muted-foreground">데이터베이스 연결 정보를 관리하세요</p>
                </div>
                
                <div className="space-y-4">
                  <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
                    <div className="space-y-2">
                      <label className="text-sm font-medium">호스트</label>
                      <input
                        type="text"
                        defaultValue="localhost"
                        className="w-full px-3 py-2 bg-muted/50 border border-border rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/50"
                      />
                    </div>
                    <div className="space-y-2">
                      <label className="text-sm font-medium">포트</label>
                      <input
                        type="number"
                        defaultValue="3307"
                        className="w-full px-3 py-2 bg-muted/50 border border-border rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/50"
                      />
                    </div>
                    <div className="space-y-2">
                      <label className="text-sm font-medium">데이터베이스명</label>
                      <input
                        type="text"
                        defaultValue="first_ent"
                        className="w-full px-3 py-2 bg-muted/50 border border-border rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/50"
                      />
                    </div>
                    <div className="space-y-2">
                      <label className="text-sm font-medium">사용자명</label>
                      <input
                        type="text"
                        defaultValue="first_ent_user"
                        className="w-full px-3 py-2 bg-muted/50 border border-border rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/50"
                      />
                    </div>
                    <div className="space-y-2 md:col-span-2">
                      <label className="text-sm font-medium">비밀번호</label>
                      <input
                        type="password"
                        placeholder="데이터베이스 비밀번호"
                        className="w-full px-3 py-2 bg-muted/50 border border-border rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/50"
                      />
                    </div>
                  </div>
                </div>
              </div>
            )}
            
            {activeTab === 'notifications' && (
              <div className="space-y-6">
                <div>
                  <h2 className="text-xl font-semibold mb-2">알림 설정</h2>
                  <p className="text-muted-foreground">알림 설정을 관리하세요</p>
                </div>
                
                <div className="space-y-4">
                  <div className="flex items-center justify-between p-4 border border-border rounded-xl">
                    <div>
                      <p className="font-medium">이메일 알림</p>
                      <p className="text-sm text-muted-foreground">중요한 업데이트를 이메일로 받습니다</p>
                    </div>
                    <input type="checkbox" defaultChecked className="w-4 h-4" />
                  </div>
                  <div className="flex items-center justify-between p-4 border border-border rounded-xl">
                    <div>
                      <p className="font-medium">채널 동기화 알림</p>
                      <p className="text-sm text-muted-foreground">채널 동기화 완료 시 알림을 받습니다</p>
                    </div>
                    <input type="checkbox" defaultChecked className="w-4 h-4" />
                  </div>
                  <div className="flex items-center justify-between p-4 border border-border rounded-xl">
                    <div>
                      <p className="font-medium">시스템 업데이트 알림</p>
                      <p className="text-sm text-muted-foreground">시스템 업데이트 시 알림을 받습니다</p>
                    </div>
                    <input type="checkbox" className="w-4 h-4" />
                  </div>
                </div>
              </div>
            )}
            
            {activeTab === 'security' && (
              <div className="space-y-6">
                <div>
                  <h2 className="text-xl font-semibold mb-2">보안 설정</h2>
                  <p className="text-muted-foreground">계정 보안을 관리하세요</p>
                </div>
                
                <div className="space-y-4">
                  <div className="space-y-2">
                    <label className="text-sm font-medium">현재 비밀번호</label>
                    <input
                      type="password"
                      placeholder="현재 비밀번호를 입력하세요"
                      className="w-full px-3 py-2 bg-muted/50 border border-border rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/50"
                    />
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm font-medium">새 비밀번호</label>
                    <input
                      type="password"
                      placeholder="새 비밀번호를 입력하세요"
                      className="w-full px-3 py-2 bg-muted/50 border border-border rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/50"
                    />
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm font-medium">비밀번호 확인</label>
                    <input
                      type="password"
                      placeholder="새 비밀번호를 다시 입력하세요"
                      className="w-full px-3 py-2 bg-muted/50 border border-border rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/50"
                    />
                  </div>
                </div>
              </div>
            )}
            
            {activeTab === 'general' && (
              <div className="space-y-6">
                <div>
                  <h2 className="text-xl font-semibold mb-2">일반 설정</h2>
                  <p className="text-muted-foreground">일반적인 시스템 설정을 관리하세요</p>
                </div>
                
                <div className="space-y-4">
                  <div className="space-y-2">
                    <label className="text-sm font-medium">언어</label>
                    <select className="w-full px-3 py-2 bg-muted/50 border border-border rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/50">
                      <option value="ko">한국어</option>
                      <option value="en">English</option>
                    </select>
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm font-medium">시간대</label>
                    <select className="w-full px-3 py-2 bg-muted/50 border border-border rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/50">
                      <option value="Asia/Seoul">Asia/Seoul (UTC+9)</option>
                      <option value="UTC">UTC</option>
                    </select>
                  </div>
                  <div className="space-y-2">
                    <label className="text-sm font-medium">테마</label>
                    <select className="w-full px-3 py-2 bg-muted/50 border border-border rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/50">
                      <option value="dark">다크 모드</option>
                      <option value="light">라이트 모드</option>
                      <option value="auto">자동</option>
                    </select>
                  </div>
                </div>
              </div>
            )}
            
            <div className="flex justify-end pt-6 border-t border-border">
              <button className="flex items-center space-x-2 px-6 py-2 bg-primary text-primary-foreground rounded-xl hover:bg-primary/90 transition-colors">
                <Save className="w-4 h-4" />
                <span>설정 저장</span>
              </button>
            </div>
          </div>
        </div>
      </div>
    </div>
  )
}

export default Settings
