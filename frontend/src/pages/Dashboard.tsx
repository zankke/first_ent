import React, { useState, useEffect } from 'react'
import { Users, Radio, TrendingUp, Activity, Instagram, Youtube, Link } from 'lucide-react'

const Dashboard = () => {
  const [stats, setStats] = useState([])
  const [statsLoading, setStatsLoading] = useState(true)
  const [statsError, setStatsError] = useState(null)

  const fetchStats = async () => {
    setStatsLoading(true)
    setStatsError(null)
    try {
      // const response = await fetch('http://localhost:5001/api/dashboard/stats')
      const response = await fetch('/api/dashboard/stats')
      if (!response.ok) {
        throw new Error('Network response was not ok')
      }
      const data = await response.json()
      setStats(data)
    } catch (error) {
      console.error('Error fetching dashboard stats:', error)
      setStatsError('통계 데이터를 불러오는 데 실패했습니다.')
    } finally {
      setStatsLoading(false)
    }
  }

  const [recentArtists, setRecentArtists] = useState([])
  const [recentArtistsLoading, setRecentArtistsLoading] = useState(true)
  const [recentArtistsError, setRecentArtistsError] = useState(null)

  const fetchRecentArtists = async () => {
    setRecentArtistsLoading(true)
    setRecentArtistsError(null)
    try {
      //const response = await fetch('http://localhost:5001/api/artists/recent')
      const response = await fetch('/api/artists/recent')
      if (!response.ok) {
        throw new Error('Network response was not ok')
      }
      const data = await response.json()
      setRecentArtists(data)
    } catch (error) {
      console.error('Error fetching recent artists:', error)
      setRecentArtistsError('최근 아티스트 데이터를 불러오는 데 실패했습니다.')
    } finally {
      setRecentArtistsLoading(false)
    }
  }

  const [channelPerformance, setChannelPerformance] = useState([])
  const [channelPerformanceLoading, setChannelPerformanceLoading] = useState(true)
  const [channelPerformanceError, setChannelPerformanceError] = useState(null)

  const fetchChannelPerformance = async () => {
    setChannelPerformanceLoading(true)
    setChannelPerformanceError(null)
    try {
      // const response = await fetch('http://localhost:5001/api/dashboard/channel-performance')
      const response = await fetch('/api/dashboard/channel-performance')
      if (!response.ok) {
        throw new Error('Network response was not ok')
      }
      const data = await response.json()
      setChannelPerformance(data)
    } catch (error) {
      console.error('Error fetching channel performance:', error)
      setChannelPerformanceError('채널 성과 데이터를 불러오는 데 실패했습니다.')
    } finally {
      setChannelPerformanceLoading(false)
    }
  }

  const [recentNews, setRecentNews] = useState([])
  const [recentNewsLoading, setRecentNewsLoading] = useState(true)
  const [recentNewsError, setRecentNewsError] = useState(null)

  const fetchRecentNews = async () => {
    setRecentNewsLoading(true)
    setRecentNewsError(null)
    try {
      const response = await fetch('/api/news?days=365&per_page=5') // Fetch 5 recent news items from the last year
      if (!response.ok) {
        throw new Error('Network response was not ok')
      }
      const data = await response.json()
      setRecentNews(data.news)
    } catch (error) {
      console.error('Error fetching recent news:', error)
      setRecentNewsError('최근 뉴스 데이터를 불러오는 데 실패했습니다.')
    } finally {
      setRecentNewsLoading(false)
    }
  }

  useEffect(() => {
    fetchStats()
    fetchRecentArtists()
    fetchChannelPerformance()
    fetchRecentNews() // Fetch recent news on component mount
  }, [])

  const iconMap = {
    Users,
    Radio,
    TrendingUp,
    Activity,
    Instagram,
    Youtube,
    Link,
  };

  return (
    <div className="space-y-6">
      <div>
        <h1 className="text-3xl font-bold gradient-text mb-2">Dashboard</h1>
        <p className="text-muted-foreground">[First Ent] AI 기반 Artist 관리 시스템에 오신 것을 환영합니다</p>
      </div>
      
      {/* 통계 카드 */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
        {statsLoading && <div className="col-span-full text-center text-gray-400">통계 데이터를 불러오는 중...</div>}
        {statsError && <div className="col-span-full text-center text-red-500">{statsError}</div>}
        {!statsLoading && !statsError && stats.length > 0 && stats.map((stat, index) => {
          const Icon = iconMap[stat.icon] // Use the icon map
          return (
            <div key={index} className="glass rounded-2xl p-6">
              <div className="flex items-center justify-between mb-4">
                <div className={`w-12 h-12 bg-gradient-to-r ${stat.color} rounded-xl flex items-center justify-center`}>
                  {/* Dynamically render icon based on string name */}
                  {Icon && React.createElement(Icon, { className: "w-6 h-6 text-white" })}
                </div>
                <span className={`text-sm font-medium ${
                  stat.changeType === 'positive' ? 'text-green-500' : 'text-red-500'
                }`}>
                  {stat.change}
                </span>
              </div>
              <div>
                <p className="text-2xl font-bold">{stat.value}</p>
                <p className="text-sm text-muted-foreground">{stat.title}</p>
              </div>
            </div>
          )
        })}
      </div>
      
      {/* 최근 활동 */}
      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="glass rounded-2xl p-6">
          <h3 className="text-lg font-semibold mb-4">최근 등록된 아티스트</h3>
          {recentArtistsLoading && <div className="text-center text-gray-400">최근 아티스트를 불러오는 중...</div>}
          {recentArtistsError && <div className="text-center text-red-500">{recentArtistsError}</div>}
          {!recentArtistsLoading && !recentArtistsError && recentArtists.length === 0 && (
            <div className="text-center text-gray-400">최근 등록된 아티스트가 없습니다.</div>
          )}
          {!recentArtistsLoading && !recentArtistsError && recentArtists.length > 0 && (
            <div className="space-y-3">
              {recentArtists.map((artist, index) => (
                <div key={index} className="flex items-center justify-between p-3 rounded-xl bg-muted/30">
                  <div className="flex items-center space-x-3">
                    {artist.profile_photo ? (
                      <img src={artist.profile_photo} alt={artist.name} className="w-10 h-10 object-cover rounded-full" />
                    ) : (
                      <div className="w-10 h-10 bg-gradient-to-r from-purple-500 to-pink-500 rounded-full flex items-center justify-center">
                        <span className="text-sm font-bold text-white">{artist.name[0]}</span>
                      </div>
                    )}
                    <div>
                      <p className="font-medium">{artist.name}</p>
                      {artist.channels && artist.channels.map((channel, channelIndex) => (
                        <p key={channelIndex} className="text-sm text-muted-foreground">
                          {channel.platform}: {channel.followers}
                        </p>
                      ))}
                    </div>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
        
        <div className="glass rounded-2xl p-6">
          <h3 className="text-lg font-semibold mb-4">채널 성과</h3>
          {channelPerformanceLoading && <div className="text-center text-gray-400">채널 성과 데이터를 불러오는 중...</div>}
          {channelPerformanceError && <div className="text-center text-red-500">{channelPerformanceError}</div>}
          {!channelPerformanceLoading && !channelPerformanceError && channelPerformance.length === 0 && (
            <div className="text-center text-gray-400">채널 성과 데이터가 없습니다.</div>
          )}
          {!channelPerformanceLoading && !channelPerformanceError && channelPerformance.length > 0 && (
            <div className="space-y-4">
              {channelPerformance.map((channel, index) => (
                <div key={index} className="flex items-center justify-between">
                  <div className="flex items-center space-x-3">
                    <div className="w-8 h-8 bg-gradient-to-r from-blue-500 to-purple-500 rounded-lg flex items-center justify-center">
                      <Radio className="w-4 h-4 text-white" />
                    </div>
                    <span className="font-medium">{channel.platform}</span>
                  </div>
                  <div className="text-right">
                    <p className="text-sm font-medium text-green-500">{channel.growth}</p>
                    <p className="text-xs text-muted-foreground">{channel.posts} posts</p>
                  </div>
                </div>
              ))}
            </div>
          )}
        </div>
      </div>

      {/* 최신 뉴스 */}
      <div className="glass rounded-2xl p-6">
        <h3 className="text-lg font-semibold mb-4">최신 뉴스</h3>
        {recentNewsLoading && <div className="text-center text-gray-400">최신 뉴스를 불러오는 중...</div>}
        {recentNewsError && <div className="text-center text-red-500">{recentNewsError}</div>}
        {!recentNewsLoading && !recentNewsError && recentNews.length === 0 && (
          <div className="text-center text-gray-400">최신 뉴스가 없습니다.</div>
        )}
        {!recentNewsLoading && !recentNewsError && recentNews.length > 0 && (
          <div className="space-y-4">
            {recentNews.map((newsItem, index) => (
              <a href={newsItem.url} target="_blank" rel="noopener noreferrer" key={index} className="flex items-start space-x-4 p-3 rounded-xl bg-muted/30 hover:bg-muted/50 transition-colors">
                {newsItem.thumbnail && (
                  <img src={newsItem.thumbnail} alt="News thumbnail" className="w-20 h-20 object-cover rounded-lg flex-shrink-0" />
                )}
                <div className="flex-grow">
                  <p className="font-medium text-sm mb-1">{newsItem.title}</p>
                  <p className="text-xs text-muted-foreground line-clamp-2">{newsItem.content}</p>
                  <p className="text-xs text-gray-500 mt-1">{newsItem.media_name} - {new Date(newsItem.published_at).toLocaleDateString()}</p>
                </div>
              </a>
            ))}
          </div>
        )}
      </div>
    </div>
  )
}

export default Dashboard