import React, { useState, useEffect, useContext } from 'react'
import { Plus, Search, Edit, Trash2, Eye, MessageSquare, X, Check } from 'lucide-react'
import { AuthContext } from '../context/AuthContext'
import { toast } from 'sonner'

interface BoardPost {
  id: number
  title: string
  content: string
  author_id: number
  author_name: string
  board_type: 'notice' | 'announcement' | 'general'
  is_published: boolean
  view_count: number
  created_at: string
  updated_at: string
}

const Boards = () => {
  const authContext = useContext(AuthContext)
  const session = authContext?.session
  const user = authContext?.user

  const [boards, setBoards] = useState<BoardPost[]>([])
  const [loading, setLoading] = useState(true)
  const [searchQuery, setSearchQuery] = useState('')
  const [filterType, setFilterType] = useState<string>('')
  
  // Modal states
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [currentPost, setCurrentPost] = useState<Partial<BoardPost> | null>(null)
  const [isEditing, setIsEditing] = useState(false)

  const fetchBoards = async () => {
    setLoading(true)
    try {
      let url = `/api/boards/?query=${encodeURIComponent(searchQuery)}`
      if (filterType) url += `&board_type=${filterType}`
      
      const response = await fetch(url)
      if (response.ok) {
        const data = await response.json()
        setBoards(data.boards)
      } else {
        toast.error('게시글을 불러오는데 실패했습니다.')
      }
    } catch (error) {
      console.error('Error fetching boards:', error)
      toast.error('서버 연결 오류가 발생했습니다.')
    } finally {
      setLoading(false)
    }
  }

  useEffect(() => {
    fetchBoards()
  }, [searchQuery, filterType])

  const handleCreatePost = () => {
    setCurrentPost({
      title: '',
      content: '',
      board_type: 'general',
      is_published: true
    })
    setIsEditing(false)
    setIsModalOpen(true)
  }

  const handleEditPost = (post: BoardPost) => {
    setCurrentPost(post)
    setIsEditing(true)
    setIsModalOpen(true)
  }

  const handleDeletePost = async (id: number) => {
    if (!window.confirm('정말 이 게시글을 삭제하시겠습니까?')) return

    try {
      const response = await fetch(`/api/boards/${id}`, {
        method: 'DELETE',
        headers: {
          'Authorization': `Bearer ${session?.access_token}`
        }
      })

      if (response.ok) {
        toast.success('게시글이 삭제되었습니다.')
        fetchBoards()
      } else {
        toast.error('삭제에 실패했습니다.')
      }
    } catch (error) {
      toast.error('오류가 발생했습니다.')
    }
  }

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!currentPost?.title || !currentPost?.content) {
      toast.error('제목과 내용을 입력해주세요.')
      return
    }

    try {
      const url = isEditing ? `/api/boards/${currentPost.id}` : '/api/boards/'
      const method = isEditing ? 'PUT' : 'POST'
      
      const payload = {
        ...currentPost,
        author_id: user?.uqid || 1 // Fallback to 1 if not logged in for testing
      }

      const response = await fetch(url, {
        method,
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${session?.access_token}`
        },
        body: JSON.stringify(payload)
      })

      if (response.ok) {
        toast.success(isEditing ? '게시글이 수정되었습니다.' : '게시글이 작성되었습니다.')
        setIsModalOpen(false)
        fetchBoards()
      } else {
        const errorData = await response.json()
        toast.error(errorData.error || '저장에 실패했습니다.')
      }
    } catch (error) {
      toast.error('오류가 발생했습니다.')
    }
  }

  const getBoardTypeColor = (type: string) => {
    switch (type) {
      case 'notice': return 'from-red-500 to-pink-500'
      case 'announcement': return 'from-blue-500 to-cyan-500'
      case 'general': return 'from-green-500 to-emerald-500'
      default: return 'from-gray-500 to-gray-700'
    }
  }

  const getBoardTypeLabel = (type: string) => {
    switch (type) {
      case 'notice': return '공지사항'
      case 'announcement': return '알림'
      case 'general': return '일반'
      default: return type
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold gradient-text mb-2">게시판 관리</h1>
          <p className="text-muted-foreground">공지사항과 게시글을 관리하세요</p>
        </div>
        <button 
          onClick={handleCreatePost}
          className="flex items-center space-x-2 px-4 py-2 bg-primary text-primary-foreground rounded-xl hover:bg-primary/90 transition-all hover:scale-105 active:scale-95 shadow-lg shadow-primary/20"
        >
          <Plus className="w-4 h-4" />
          <span>새 게시글 작성</span>
        </button>
      </div>
      
      {/* 검색 및 필터 */}
      <div className="glass rounded-2xl p-6">
        <div className="flex flex-col md:flex-row items-center gap-4">
          <div className="relative flex-1 w-full">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-4 h-4" />
            <input
              type="text"
              placeholder="게시글 제목 또는 내용 검색..."
              className="w-full pl-10 pr-4 py-2 bg-muted/50 border border-border rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/50 transition-all"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
            />
          </div>
          <div className="flex items-center gap-2 w-full md:w-auto">
            <select 
              className="px-4 py-2 bg-muted/50 border border-border rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/50 appearance-none min-w-[120px]"
              value={filterType}
              onChange={(e) => setFilterType(e.target.value)}
            >
              <option value="">모든 유형</option>
              <option value="notice">공지사항</option>
              <option value="announcement">알림</option>
              <option value="general">일반</option>
            </select>
            <button 
              onClick={() => {setSearchQuery(''); setFilterType('');}}
              className="px-4 py-2 border border-border rounded-xl hover:bg-muted/50 transition-colors whitespace-nowrap"
            >
              초기화
            </button>
          </div>
        </div>
      </div>
      
      {/* 게시글 목록 */}
      <div className="space-y-4">
        {loading ? (
          <div className="flex flex-col items-center justify-center py-20 space-y-4">
            <div className="w-10 h-10 border-4 border-primary border-t-transparent rounded-full animate-spin"></div>
            <p className="text-muted-foreground animate-pulse">게시글을 불러오는 중...</p>
          </div>
        ) : boards.length === 0 ? (
          <div className="glass rounded-2xl p-20 text-center space-y-4">
            <MessageSquare className="w-12 h-12 text-muted-foreground mx-auto opacity-20" />
            <p className="text-muted-foreground">게시글이 없습니다.</p>
          </div>
        ) : (
          boards.map((board) => (
            <div key={board.id} className="glass rounded-2xl p-6 hover:shadow-xl transition-all duration-300 border-white/5 group relative overflow-hidden">
              <div className="absolute top-0 left-0 w-1 h-full bg-gradient-to-b opacity-0 group-hover:opacity-100 transition-opacity" style={{ backgroundImage: `linear-gradient(to bottom, var(--tw-gradient-from), var(--tw-gradient-to))` }}></div>
              
              <div className="flex items-start justify-between mb-4">
                <div className="flex items-center space-x-4">
                  <div className={`w-12 h-12 bg-gradient-to-br ${getBoardTypeColor(board.board_type)} rounded-2xl flex items-center justify-center shadow-lg shadow-black/20 transform group-hover:rotate-12 transition-transform`}>
                    <MessageSquare className="w-6 h-6 text-white" />
                  </div>
                  <div>
                    <h3 className="font-bold text-xl group-hover:text-primary transition-colors">{board.title}</h3>
                    <div className="flex items-center space-x-3 mt-1.5">
                      <span className={`px-2.5 py-0.5 rounded-lg text-[10px] font-black uppercase tracking-wider bg-gradient-to-r ${getBoardTypeColor(board.board_type)} text-white shadow-sm`}>
                        {getBoardTypeLabel(board.board_type)}
                      </span>
                      <span className="text-xs text-muted-foreground font-medium">by <span className="text-foreground">{board.author_name}</span></span>
                      <span className="text-muted-foreground/30">•</span>
                      <span className="text-xs text-muted-foreground">{new Date(board.created_at).toLocaleDateString()}</span>
                    </div>
                  </div>
                </div>
                <div className="flex items-center space-x-2">
                  {board.is_published ? (
                    <span className="px-3 py-1 rounded-full text-[10px] font-bold bg-green-500/10 text-green-500 border border-green-500/20 uppercase tracking-widest">
                      Published
                    </span>
                  ) : (
                    <span className="px-3 py-1 rounded-full text-[10px] font-bold bg-yellow-500/10 text-yellow-500 border border-yellow-500/20 uppercase tracking-widest">
                      Draft
                    </span>
                  )}
                </div>
              </div>
              
              <p className="text-muted-foreground mb-6 line-clamp-2 leading-relaxed text-sm">{board.content}</p>
              
              <div className="flex items-center justify-between pt-4 border-t border-white/5">
                <div className="flex items-center space-x-6 text-xs text-muted-foreground font-medium">
                  <div className="flex items-center space-x-1.5 group/stat">
                    <Eye className="w-4 h-4 group-hover/stat:text-primary transition-colors" />
                    <span>{board.view_count} views</span>
                  </div>
                </div>
                <div className="flex items-center space-x-1">
                  <button 
                    onClick={() => handleEditPost(board)}
                    className="p-2.5 text-muted-foreground hover:text-primary hover:bg-primary/10 rounded-xl transition-all"
                    title="수정"
                  >
                    <Edit className="w-4 h-4" />
                  </button>
                  <button 
                    onClick={() => handleDeletePost(board.id)}
                    className="p-2.5 text-muted-foreground hover:text-destructive hover:bg-destructive/10 rounded-xl transition-all"
                    title="삭제"
                  >
                    <Trash2 className="w-4 h-4" />
                  </button>
                </div>
              </div>
            </div>
          ))
        )}
      </div>

      {/* Write/Edit Modal */}
      {isModalOpen && (
        <div className="fixed inset-0 z-50 flex items-center justify-center p-4 bg-black/60 backdrop-blur-sm animate-in fade-in duration-200">
          <div className="glass w-full max-w-2xl rounded-[2rem] shadow-2xl border-white/10 overflow-hidden animate-in zoom-in-95 duration-200">
            <div className="p-8 border-b border-white/5 flex items-center justify-between bg-gradient-to-r from-slate-900 to-slate-950">
              <div>
                <h2 className="text-2xl font-bold text-white tracking-tight">
                  {isEditing ? '게시글 수정' : '새 게시글 작성'}
                </h2>
                <p className="text-xs text-muted-foreground mt-1 uppercase tracking-[0.2em] font-bold">BBS Management System</p>
              </div>
              <button 
                onClick={() => setIsModalOpen(false)}
                className="p-2 hover:bg-white/5 rounded-full transition-colors text-muted-foreground hover:text-white"
              >
                <X className="w-6 h-6" />
              </button>
            </div>
            
            <form onSubmit={handleSubmit} className="p-8 space-y-6 bg-slate-950/50">
              <div className="space-y-2">
                <label className="text-[10px] font-black uppercase tracking-widest text-muted-foreground ml-1">Title</label>
                <input
                  type="text"
                  placeholder="게시글 제목을 입력하세요"
                  className="w-full px-5 py-4 bg-white/5 border border-white/10 rounded-2xl focus:outline-none focus:ring-2 focus:ring-primary/50 text-white font-medium transition-all"
                  value={currentPost?.title || ''}
                  onChange={(e) => setCurrentPost({...currentPost, title: e.target.value})}
                  required
                />
              </div>
              
              <div className="grid grid-cols-2 gap-6">
                <div className="space-y-2">
                  <label className="text-[10px] font-black uppercase tracking-widest text-muted-foreground ml-1">Type</label>
                  <select 
                    className="w-full px-5 py-4 bg-white/5 border border-white/10 rounded-2xl focus:outline-none focus:ring-2 focus:ring-primary/50 text-white transition-all appearance-none"
                    value={currentPost?.board_type || 'general'}
                    onChange={(e) => setCurrentPost({...currentPost, board_type: e.target.value as any})}
                  >
                    <option value="general">일반</option>
                    <option value="notice">공지사항</option>
                    <option value="announcement">알림</option>
                  </select>
                </div>
                <div className="space-y-2">
                  <label className="text-[10px] font-black uppercase tracking-widest text-muted-foreground ml-1">Visibility</label>
                  <div className="flex items-center h-[60px] px-5 bg-white/5 border border-white/10 rounded-2xl">
                    <label className="flex items-center cursor-pointer w-full justify-between">
                      <span className="text-sm font-medium text-white">바로 발행하기</span>
                      <input 
                        type="checkbox" 
                        className="hidden peer"
                        checked={currentPost?.is_published || false}
                        onChange={(e) => setCurrentPost({...currentPost, is_published: e.target.checked})}
                      />
                      <div className="w-10 h-6 bg-white/10 rounded-full peer-checked:bg-primary relative transition-colors">
                        <div className="absolute top-1 left-1 w-4 h-4 bg-white rounded-full transition-transform peer-checked:translate-x-4"></div>
                      </div>
                    </label>
                  </div>
                </div>
              </div>
              
              <div className="space-y-2">
                <label className="text-[10px] font-black uppercase tracking-widest text-muted-foreground ml-1">Content</label>
                <textarea
                  placeholder="게시글 내용을 입력하세요"
                  rows={8}
                  className="w-full px-5 py-4 bg-white/5 border border-white/10 rounded-2xl focus:outline-none focus:ring-2 focus:ring-primary/50 text-white font-light leading-relaxed transition-all resize-none"
                  value={currentPost?.content || ''}
                  onChange={(e) => setCurrentPost({...currentPost, content: e.target.value})}
                  required
                />
              </div>
              
              <div className="flex gap-4 pt-4">
                <button
                  type="button"
                  onClick={() => setIsModalOpen(false)}
                  className="flex-1 py-4 px-6 border border-white/10 rounded-2xl text-white font-bold hover:bg-white/5 transition-all active:scale-95"
                >
                  취소
                </button>
                <button
                  type="submit"
                  className="flex-1 py-4 px-6 bg-primary text-primary-foreground rounded-2xl font-black uppercase tracking-widest hover:bg-primary/90 transition-all active:scale-95 shadow-xl shadow-primary/20 flex items-center justify-center gap-2"
                >
                  <Check className="w-5 h-5" />
                  {isEditing ? '수정 완료' : '게시글 작성'}
                </button>
              </div>
            </form>
          </div>
        </div>
      )}
    </div>
  )
}

export default Boards
