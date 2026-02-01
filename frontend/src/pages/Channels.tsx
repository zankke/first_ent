import { useState, useEffect } from 'react'
import { Plus, Search, Filter, MoreVertical, Edit, RefreshCw, ExternalLink } from 'lucide-react'

const formatNumberToK_M = (num: number | null | undefined): string => {
  if (num === null || num === undefined) {
    return "N/A"
  }
  if (num >= 1_000_000) {
    return `${(num / 1_000_000).toFixed(1)}M`
  }
  if (num >= 1_000) {
    return `${(num / 1_000).toFixed(1)}K`
  }
  return String(num)
}

const Channels = () => {
  const [channels, setChannels] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState(null)

  useEffect(() => {
    const fetchChannels = async () => {
      setLoading(true)
      setError(null)
      try {
        const response = await fetch('/api/channels')
        if (!response.ok) {
          throw new Error('Network response was not ok')
        }
        const data = await response.json()
        setChannels(data.channels)
      } catch (err: any) {
        console.error('Error fetching channels:', err)
        setError(err.message)
      } finally {
        setLoading(false)
      }
    }
    fetchChannels()
  }, [])

  const getPlatformColor = (platform: string) => {
    switch (platform) {
      case 'instagram': return 'from-pink-500 to-purple-500'
      case 'youtube': return 'from-red-500 to-pink-500'
      case 'tiktok': return 'from-black to-gray-800'
      case 'twitter': return 'from-blue-400 to-blue-600'
      default: return 'from-gray-500 to-gray-700'
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold gradient-text mb-2">채널 관리</h1>
          <p className="text-muted-foreground">소셜미디어 채널을 모니터링하고 관리하세요</p>
        </div>
        <button className="flex items-center space-x-2 px-4 py-2 bg-primary text-primary-foreground rounded-xl hover:bg-primary/90 transition-colors">
          <Plus className="w-4 h-4" />
          <span>새 채널 추가</span>
        </button>
      </div>
      
      {/* 검색 및 필터 */}
      <div className="glass rounded-2xl p-6">
        <div className="flex items-center space-x-4">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-4 h-4" />
            <input
              type="text"
              placeholder="채널 검색..."
              className="w-full pl-10 pr-4 py-2 bg-muted/50 border border-border rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/50"
            />
          </div>
          <button className="flex items-center space-x-2 px-4 py-2 border border-border rounded-xl hover:bg-muted/50 transition-colors">
            <Filter className="w-4 h-4" />
            <span>필터</span>
          </button>
        </div>
      </div>
      
      {/* 채널 목록 */}
      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {loading && <div className="col-span-full text-center text-gray-400">채널 데이터를 불러오는 중...</div>}
        {error && <div className="col-span-full text-center text-red-500">채널 데이터를 불러오는 데 실패했습니다: {error}</div>}
        {!loading && !error && channels.length === 0 && (
          <div className="col-span-full text-center text-gray-400">등록된 채널이 없습니다.</div>
        )}
        {!loading && !error && channels.length > 0 && channels.map((channel: any) => (
          <div key={channel.id} className="glass rounded-2xl p-6 hover:shadow-lg transition-all duration-200">
            <div className="flex items-center justify-between mb-4">
              <div className="flex items-center space-x-3">
                <div className={`w-12 h-12 bg-gradient-to-r ${getPlatformColor(channel.platform)} rounded-xl flex items-center justify-center`}>
                  <span className="text-white font-bold text-lg">{channel.platform[0].toUpperCase()}</span>
                </div>
                <div>
                  <p className="font-medium">{channel.channel_name || 'N/A'}</p>
                  <p className="text-sm text-muted-foreground">{channel.artist_name || 'N/A'}</p>
                </div>
              </div>
              <div className="flex items-center space-x-1">
                {channel.is_verified && (
                  <span className="w-2 h-2 bg-blue-500 rounded-full"></span>
                )}
                <button className="p-1 text-muted-foreground hover:text-foreground transition-colors">
                  <MoreVertical className="w-4 h-4" />
                </button>
              </div>
            </div>
            
            <div className="space-y-3 mb-4">
              <div className="flex justify-between">
                <span className="text-sm text-muted-foreground">팔로워</span>
                <span className="font-medium">{formatNumberToK_M(channel.follower_count)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-muted-foreground">팔로잉</span>
                <span className="font-medium">{formatNumberToK_M(channel.following_count)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-muted-foreground">게시물</span>
                <span className="font-medium">{formatNumberToK_M(channel.post_count)}</span>
              </div>
              <div className="flex justify-between">
                <span className="text-sm text-muted-foreground">마지막 동기화</span>
                <span className="text-sm text-muted-foreground">{channel.last_sync_at ? new Date(channel.last_sync_at).toLocaleString() : 'N/A'}</span>
              </div>
            </div>
            
            <div className="flex items-center space-x-2">
              <button className="flex-1 flex items-center justify-center space-x-2 px-3 py-2 bg-muted/50 rounded-xl hover:bg-muted transition-colors">
                <RefreshCw className="w-4 h-4" />
                <span className="text-sm">동기화</span>
              </button>
              <button className="flex items-center justify-center space-x-2 px-3 py-2 border border-border rounded-xl hover:bg-muted transition-colors">
                <ExternalLink className="w-4 h-4" />
              </button>
              <button className="flex items-center justify-center space-x-2 px-3 py-2 border border-border rounded-xl hover:bg-muted transition-colors">
                <Edit className="w-4 h-4" />
              </button>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Channels
