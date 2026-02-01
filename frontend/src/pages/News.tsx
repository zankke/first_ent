import React, { useState, useEffect, Component, ErrorInfo, ReactNode } from 'react'
import { Search, Filter, RefreshCw, ExternalLink, Calendar, User, TrendingUp, Clock, Play, Pause, Eye, EyeOff } from 'lucide-react'
import Pagination from '../components/Pagination' // Import Pagination component

interface NewsArticle {
  id: number
  artist_name: string
  title: string
  content: string
  url: string
  source: string
  published_at: string
  crawled_at: string
  sentiment: 'positive' | 'negative' | 'neutral'
  relevance_score: number
  keywords: string[]
  thumbnail?: string
  media_name?: string
  isVisible?: boolean; // New field for toggle visibility
}

interface NewsStats {
  total_news: number
  recent_news: number
  artist_news_counts: Array<{
    id: number
    artist_name: string
    news_count: number
  }>
  sentiment_counts: Array<{
    sentiment: string
    count: number
  }>
}

interface ErrorBoundaryProps {
  children: ReactNode;
}

interface ErrorBoundaryState {
  hasError: boolean;
}

class ErrorBoundary extends Component<ErrorBoundaryProps, ErrorBoundaryState> {
  constructor(props: ErrorBoundaryProps) {
    super(props);
    this.state = { hasError: false };
  }

  static getDerivedStateFromError(_: Error): ErrorBoundaryState {
    return { hasError: true };
  }

  componentDidCatch(error: Error, info: ErrorInfo) {
    console.error("ErrorBoundary caught an error", error, info);
  }

  render() {
    if (this.state.hasError) {
      return <h2>Something went wrong.</h2>;
    }

    return this.props.children;
  }
}

const News = () => {
  const [news, setNews] = useState<NewsArticle[]>([])
  const [stats, setStats] = useState<NewsStats | null>(null)
  const [loading, setLoading] = useState(true)
  const [schedulerStatus, setSchedulerStatus] = useState({ is_running: false, next_run_time: '' })
  const [selectedArtist, setSelectedArtist] = useState('')
  const [selectedSentiment, setSelectedSentiment] = useState('')
  const [days, setDays] = useState(365) // Changed default from 7 to 365
  const [searchQuery, setSearchQuery] = useState('')
  const [showSampleNews, setShowSampleNews] = useState(false) // New state for toggle
  const [showNewsList, setShowNewsList] = useState(true) // New state for news list visibility
  const [currentPage, setCurrentPage] = useState(1) // New state for current page
  const [totalPages, setTotalPages] = useState(1)     // New state for total pages
  const [perPage, setPerPage] = useState(10)           // New state for items per page
  const [newsItemVisibility, setNewsItemVisibility] = useState<Map<number, boolean>>(new Map()); // New state for individual news item visibility

  useEffect(() => {
    setCurrentPage(1)
  }, [selectedArtist, selectedSentiment, days, searchQuery, showSampleNews])

  useEffect(() => {
    fetchNews()
    fetchStats()
    fetchSchedulerStatus()
  }, [selectedArtist, selectedSentiment, days, searchQuery, showSampleNews, currentPage, perPage]) // Add showSampleNews, currentPage and perPage to dependencies

  useEffect(() => {
    if (stats && selectedArtist) {
      const artistExists = stats.artist_news_counts.some(artist => String(artist.id) === String(selectedArtist))
      if (!artistExists) {
        setSelectedArtist('')
      }
    }
  }, [stats, selectedArtist])

  const fetchNews = async () => {
    try {
      setLoading(true)
      const params = new URLSearchParams()
      if (selectedArtist) params.append('artist_id', selectedArtist)
      if (selectedSentiment) params.append('sentiment', selectedSentiment)
      params.append('days', days.toString())
      if (searchQuery) params.append('query', searchQuery)
      if (showSampleNews) params.append('sample', 'true') // Add sample parameter
      params.append('page', currentPage.toString()) // Add page parameter
      params.append('per_page', perPage.toString()) // Add per_page parameter
      
      const response = await fetch(`/api/news?${params}`)
      const data = await response.json()
      console.log('Fetched news data:', data); // Added log
      const fetchedNews = data.news || []

      setNews(fetchedNews)
      setNewsItemVisibility(new Map(fetchedNews.map(item => [item.id, true]))); // Initialize all as visible
      setTotalPages(data.pages) // Update total pages from backend response
    } catch (error) {
      console.error('뉴스 조회 오류:', error)
      setNews([])
    } finally {
      setLoading(false)
    }
  }

  const handlePageChange = (page: number) => {
    setCurrentPage(page);
  }

  const handleToggleNewsItemVisibility = (id: number) => {
    setNewsItemVisibility(prevVisibility => {
      const newVisibility = new Map(prevVisibility);
      newVisibility.set(id, !newVisibility.get(id));
      return newVisibility;
    });
  }

  const fetchStats = async () => {
    try {
      const response = await fetch('/api/news/stats')
      const data = await response.json()
      setStats(data)
    } catch (error) {
      console.error('통계 조회 오류:', error)
      setStats({
        total_news: 0,
        recent_news: 0,
        artist_news_counts: [],
        sentiment_counts: []
      })
    }
  }

  const fetchSchedulerStatus = async () => {
    try {
      const response = await fetch('/api/news/scheduler/status')
      const data = await response.json()
      setSchedulerStatus(data)
    } catch (error) {
      console.error('스케줄러 상태 조회 오류:', error)
      setSchedulerStatus({ is_running: false, next_run_time: 'N/A' })
    }
  }

  const handleCrawlNews = async () => {
    try {
      setLoading(true)
      const response = await fetch('/api/news/crawl', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ artist_id: selectedArtist || null })
      })
      const data = await response.json()
      
      if (response.ok) {
        alert(data.message)
        fetchNews()
        fetchStats()
      } else {
        alert('오류: ' + data.error)
      }
    } catch (error) {
      console.error('뉴스 크롤링 오류:', error)
      alert('뉴스 크롤링 중 오류가 발생했습니다.')
    } finally {
      setLoading(false)
    }
  }

  const handleSchedulerToggle = async () => {
    try {
      const endpoint = schedulerStatus.is_running ? '/api/news/scheduler/stop' : '/api/news/scheduler/start'
      const response = await fetch(endpoint, { method: 'POST' })
      const data = await response.json()
      
      if (response.ok) {
        alert(data.message)
        fetchSchedulerStatus()
      } else {
        alert('오류: ' + data.error)
      }
    } catch (error) {
      console.error('스케줄러 제어 오류:', error)
      alert('스케줄러 제어 중 오류가 발생했습니다.')
    }
  }

  const getSentimentColor = (sentiment: string) => {
    switch (sentiment) {
      case 'positive': return 'text-green-500 bg-green-500/20'
      case 'negative': return 'text-red-500 bg-red-500/20'
      case 'neutral': return 'text-gray-500 bg-gray-500/20'
      default: return 'text-gray-500 bg-gray-500/20'
    }
  }

  const getSentimentLabel = (sentiment: string) => {
    switch (sentiment) {
      case 'positive': return '긍정적'
      case 'negative': return '부정적'
      case 'neutral': return '중립적'
      default: return '미분류'
    }
  }

  const formatDate = (dateString: string) => {
    return new Date(dateString).toLocaleDateString('ko-KR', {
      year: 'numeric',
      month: 'short',
      day: 'numeric',
      hour: '2-digit',
      minute: '2-digit'
    })
  }

  return (
    <ErrorBoundary>
      <div className="space-y-6">
        <div className="flex items-center justify-between">
          <div>
            <h1 className="text-3xl font-bold gradient-text mb-2">뉴스 모니터링</h1>
            <p className="text-muted-foreground">아티스트 관련 뉴스를 모니터링하고 분석하세요</p>
          </div>
          <div className="flex items-center space-x-2">
            <button
              onClick={handleSchedulerToggle}
              className={`flex items-center space-x-2 px-4 py-2 rounded-xl transition-colors ${
                schedulerStatus.is_running
                  ? 'bg-red-500 text-white hover:bg-red-600'
                  : 'bg-green-500 text-white hover:bg-green-600'
              }`}
            >
              {schedulerStatus.is_running ? <Pause className="w-4 h-4" /> : <Play className="w-4 h-4" />}
              <span>{schedulerStatus.is_running ? '스케줄러 중지' : '스케줄러 시작'}</span>
            </button>
            <button
              onClick={handleCrawlNews}
              disabled={loading}
              className="flex items-center space-x-2 px-4 py-2 bg-primary text-primary-foreground rounded-xl hover:bg-primary/90 transition-colors disabled:opacity-50"
            >
              <RefreshCw className={`w-4 h-4 ${loading ? 'animate-spin' : ''}`} />
              <span>뉴스 크롤링</span>
            </button>
          </div>
        </div>

        {/* 통계 카드 */}
        {stats && (
          <div className="grid grid-cols-1 md:grid-cols-4 gap-6">
            <div className="glass rounded-2xl p-6">
              <div className="flex items-center justify-between mb-4">
                <div className="w-12 h-12 bg-gradient-to-r from-blue-500 to-cyan-500 rounded-xl flex items-center justify-center">
                  <TrendingUp className="w-6 h-6 text-white" />
                </div>
              </div>
              <div>
                <p className="text-2xl font-bold">{stats.total_news}</p>
                <p className="text-sm text-muted-foreground">총 뉴스 수</p>
              </div>
            </div>
            
            <div className="glass rounded-2xl p-6">
              <div className="flex items-center justify-between mb-4">
                <div className="w-12 h-12 bg-gradient-to-r from-green-500 to-emerald-500 rounded-xl flex items-center justify-center">
                  <Clock className="w-6 h-6 text-white" />
                </div>
              </div>
              <div>
                <p className="text-2xl font-bold">{stats.recent_news}</p>
                <p className="text-sm text-muted-foreground">최근 7일</p>
              </div>
            </div>
            
            <div className="glass rounded-2xl p-6">
              <div className="flex items-center justify-between mb-4">
                <div className="w-12 h-12 bg-gradient-to-r from-purple-500 to-pink-500 rounded-xl flex items-center justify-center">
                  <User className="w-6 h-6 text-white" />
                </div>
              </div>
              <div>
                <p className="text-2xl font-bold">{stats.artist_news_counts.length}</p>
                <p className="text-sm text-muted-foreground">활성 아티스트</p>
              </div>
            </div>
            
            <div className="glass rounded-2xl p-6">
              <div className="flex items-center justify-between mb-4">
                <div className="w-12 h-12 bg-gradient-to-r from-orange-500 to-red-500 rounded-xl flex items-center justify-center">
                  <Calendar className="w-6 h-6 text-white" />
                </div>
              </div>
              <div>
                <p className="text-sm font-medium">다음 실행</p>
                <p className="text-xs text-muted-foreground">{schedulerStatus.next_run_time}</p>
              </div>
            </div>
          </div>
        )}

        {/* 필터 */}
        <div className="glass rounded-2xl p-6">
          <div className="flex items-center space-x-4">
            <div className="relative flex-1">
              <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-4 h-4" />
              <input
                type="text"
                placeholder="뉴스 검색... (키워드, 제목, 아티스트 이름)"
                className="w-full pl-10 pr-4 py-2 bg-muted/50 border border-border rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/50"
                value={searchQuery}
                onChange={(e) => setSearchQuery(e.target.value)}
                onKeyPress={(e) => {
                  if (e.key === 'Enter') {
                    fetchNews();
                  }
                }}
              />
            </div>
            <button
              onClick={fetchNews}
              className="flex items-center space-x-2 px-4 py-2 text-white rounded-xl hover:bg-orange-600 transition-colors"
              style={{ backgroundColor: 'rgb(237 113 4)' }}
            >
              <Search className="w-4 h-4" />
              <span>뉴스 검색</span>
            </button>
            <select
              value={selectedArtist}
              onChange={(e) => setSelectedArtist(e.target.value)}
              className="px-4 py-2 bg-muted/50 border border-border rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/50"
            >
                          <option value="">모든 아티스트</option>
                          {stats && stats.artist_news_counts && stats.artist_news_counts.map((artist) => (
                            <option key={artist.artist_name} value={artist.id}>
                              {artist.artist_name} ({artist.news_count})
                            </option>
                          ))}            </select>
            <select
              value={selectedSentiment}
              onChange={(e) => setSelectedSentiment(e.target.value)}
              className="px-4 py-2 bg-muted/50 border border-border rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/50"
            >
              <option value="">모든 감정</option>
              <option value="positive">긍정적</option>
              <option value="negative">부정적</option>
              <option value="neutral">중립적</option>
            </select>
            <select
              value={days}
              onChange={(e) => setDays(Number(e.target.value))}
              className="px-4 py-2 bg-muted/50 border border-border rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/50"
            >
              <option value={1}>최근 1일</option>
              <option value={7}>최근 7일</option>
              <option value={30}>최근 30일</option>
              <option value={90}>최근 90일</option>
            </select>
            {/* Sample News Toggle Button */}
            <label className="flex items-center space-x-2 cursor-pointer">
              <div className="relative">
                <input
                  type="checkbox"
                  className="sr-only"
                  checked={showSampleNews}
                  onChange={() => setShowSampleNews(!showSampleNews)}
                />
                <div className="block bg-muted/50 w-14 h-8 rounded-full"></div>
                <div className={`dot absolute left-1 top-1 bg-white w-6 h-6 rounded-full transition ${showSampleNews ? 'translate-x-full bg-orange-500' : ''}`}></div>
              </div>
              <div className="text-muted-foreground font-medium">샘플 뉴스 보기</div>
            </label>
            {/* News List Toggle Button */}
            <label className="flex items-center space-x-2 cursor-pointer">
              <div className="relative">
                <input
                  type="checkbox"
                  className="sr-only"
                  checked={showNewsList}
                  onChange={() => setShowNewsList(!showNewsList)}
                />
                <div className="block bg-muted/50 w-14 h-8 rounded-full"></div>
                <div className={`dot absolute left-1 top-1 bg-white w-6 h-6 rounded-full transition ${showNewsList ? 'translate-x-full bg-orange-500' : ''}`}></div>
              </div>
              <div className="text-muted-foreground font-medium">뉴스 목록 {showNewsList ? '숨기기' : '보기'}</div>
            </label>
          </div>
        </div>

        {/* 뉴스 목록 */}
        {showNewsList && (
          <div className="space-y-4">
            {loading ? (
              <div className="glass rounded-2xl p-12 text-center">
                <RefreshCw className="w-8 h-8 animate-spin mx-auto mb-4 text-primary" />
                <p className="text-muted-foreground">뉴스를 불러오는 중...</p>
              </div>
            ) : news.length === 0 ? (
              <div className="glass rounded-2xl p-12 text-center">
                <p className="text-muted-foreground">표시할 뉴스가 없습니다.</p>
              </div>
            ) : (
              news.map((article) => (
                <div key={article.id} className="glass rounded-2xl p-6 hover:shadow-lg transition-all duration-200">
                  <div className="flex items-start space-x-4">
                    {article.thumbnail ? (
                      <a href={article.url} target="_blank" rel="noopener noreferrer">
                        <img src={article.thumbnail} alt="Thumbnail" className="w-24 h-24 object-cover rounded-xl flex-shrink-0" />
                      </a>
                    ) : (
                      <a href={article.url} target="_blank" rel="noopener noreferrer">
                        <img src={`https://picsum.photos/seed/${article.id}/200/200`} alt="Placeholder Thumbnail" className="w-24 h-24 object-cover rounded-xl flex-shrink-0" />
                      </a>
                    )}
                    <div className="flex-1">
                      <div className="flex items-center justify-between mb-2">
                        <div className="flex items-center space-x-2">
                          {article.media_name && (
                            <span className="text-sm font-medium text-primary">{article.media_name}</span>
                          )}
                          <h3 className="text-lg font-semibold line-clamp-2">{article.title}</h3>
                        </div>
                        <button
                          onClick={() => handleToggleNewsItemVisibility(article.id)}
                          className="p-1 rounded-full hover:bg-muted transition-colors"
                        >
                          {newsItemVisibility.get(article.id) ? <EyeOff className="w-4 h-4" /> : <Eye className="w-4 h-4" />}
                        </button>
                      </div>
                      {newsItemVisibility.get(article.id) && (
                        <>
                          <p className="text-muted-foreground text-sm mb-3 line-clamp-3">{article.content}</p>
                          <div className="flex items-center space-x-4 text-sm text-muted-foreground">
                            <div className="flex items-center space-x-1">
                              <User className="w-4 h-4" />
                              <span>{article.artist_name}</span>
                            </div>
                            <div className="flex items-center space-x-1">
                              <Calendar className="w-4 h-4" />
                              <span>{formatDate(article.published_at || article.crawled_at)}</span>
                            </div>
                            {article.relevance_score > 0 && (
                              <div className="flex items-center space-x-1">
                                <TrendingUp className="w-4 h-4" />
                                <span>관련도: {Math.round(article.relevance_score * 100)}%</span>
                              </div>
                            )}
                            <a
                              href={article.url}
                              target="_blank"
                              rel="noopener noreferrer"
                              className="flex items-center space-x-1 text-primary hover:underline"
                            >
                              <ExternalLink className="w-4 h-4" />
                              <span>링크</span>
                            </a>
                          </div>
                        </>
                      )}
                    </div>
                  </div>
                  
                  {newsItemVisibility.get(article.id) && article.keywords && article.keywords.length > 0 && (
                    <div className="flex flex-wrap gap-2 mt-4">
                      {article.keywords.map((keyword, index) => (
                        <span
                          key={index}
                          className="px-2 py-1 bg-muted/50 rounded-lg text-xs text-muted-foreground"
                        >
                          #{keyword}
                        </span>
                      ))}
                    </div>
                  )}
                </div>
              ))
            )}
          </div>
        )}
      </div>
      {totalPages > 1 && (
        <Pagination
          currentPage={currentPage}
          totalPages={totalPages}
          onPageChange={handlePageChange}
        />
      )}
    </ErrorBoundary>
  )
}

export default News
