import React, { useState } from 'react'
import { Plus, Search, Filter, MoreVertical, Edit, Trash2, Eye, MessageSquare } from 'lucide-react'

const Boards = () => {
  const [boards] = useState([
    {
      id: 1,
      title: '새로운 아티스트 등록 안내',
      content: '새로운 아티스트 등록 프로세스가 업데이트되었습니다...',
      author: 'admin',
      board_type: 'notice',
      is_published: true,
      view_count: 156,
      created_at: '2024-01-15'
    },
    {
      id: 2,
      title: '채널 동기화 기능 개선',
      content: 'Instagram 및 YouTube 채널 동기화 기능이 개선되었습니다...',
      author: 'manager1',
      board_type: 'announcement',
      is_published: true,
      view_count: 89,
      created_at: '2024-01-14'
    },
    {
      id: 3,
      title: '일반 게시글 예시',
      content: '이것은 일반 게시글의 예시입니다...',
      author: 'viewer1',
      board_type: 'general',
      is_published: false,
      view_count: 12,
      created_at: '2024-01-13'
    }
  ])

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
        <button className="flex items-center space-x-2 px-4 py-2 bg-primary text-primary-foreground rounded-xl hover:bg-primary/90 transition-colors">
          <Plus className="w-4 h-4" />
          <span>새 게시글 작성</span>
        </button>
      </div>
      
      {/* 검색 및 필터 */}
      <div className="glass rounded-2xl p-6">
        <div className="flex items-center space-x-4">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-4 h-4" />
            <input
              type="text"
              placeholder="게시글 검색..."
              className="w-full pl-10 pr-4 py-2 bg-muted/50 border border-border rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/50"
            />
          </div>
          <button className="flex items-center space-x-2 px-4 py-2 border border-border rounded-xl hover:bg-muted/50 transition-colors">
            <Filter className="w-4 h-4" />
            <span>필터</span>
          </button>
        </div>
      </div>
      
      {/* 게시글 목록 */}
      <div className="space-y-4">
        {boards.map((board) => (
          <div key={board.id} className="glass rounded-2xl p-6 hover:shadow-lg transition-all duration-200">
            <div className="flex items-start justify-between mb-4">
              <div className="flex items-center space-x-3">
                <div className={`w-10 h-10 bg-gradient-to-r ${getBoardTypeColor(board.board_type)} rounded-xl flex items-center justify-center`}>
                  <MessageSquare className="w-5 h-5 text-white" />
                </div>
                <div>
                  <h3 className="font-semibold text-lg">{board.title}</h3>
                  <div className="flex items-center space-x-2 mt-1">
                    <span className={`px-2 py-1 rounded-full text-xs font-medium bg-gradient-to-r ${getBoardTypeColor(board.board_type)} text-white`}>
                      {getBoardTypeLabel(board.board_type)}
                    </span>
                    <span className="text-sm text-muted-foreground">by {board.author}</span>
                    <span className="text-sm text-muted-foreground">•</span>
                    <span className="text-sm text-muted-foreground">{board.created_at}</span>
                  </div>
                </div>
              </div>
              <div className="flex items-center space-x-2">
                {board.is_published ? (
                  <span className="px-2 py-1 rounded-full text-xs font-medium bg-green-500/20 text-green-500">
                    발행됨
                  </span>
                ) : (
                  <span className="px-2 py-1 rounded-full text-xs font-medium bg-yellow-500/20 text-yellow-500">
                    임시저장
                  </span>
                )}
                <button className="p-2 text-muted-foreground hover:text-foreground transition-colors">
                  <MoreVertical className="w-4 h-4" />
                </button>
              </div>
            </div>
            
            <p className="text-muted-foreground mb-4 line-clamp-2">{board.content}</p>
            
            <div className="flex items-center justify-between">
              <div className="flex items-center space-x-4 text-sm text-muted-foreground">
                <div className="flex items-center space-x-1">
                  <Eye className="w-4 h-4" />
                  <span>{board.view_count}</span>
                </div>
              </div>
              <div className="flex items-center space-x-2">
                <button className="p-2 text-muted-foreground hover:text-foreground transition-colors">
                  <Eye className="w-4 h-4" />
                </button>
                <button className="p-2 text-muted-foreground hover:text-foreground transition-colors">
                  <Edit className="w-4 h-4" />
                </button>
                <button className="p-2 text-muted-foreground hover:text-red-500 transition-colors">
                  <Trash2 className="w-4 h-4" />
                </button>
              </div>
            </div>
          </div>
        ))}
      </div>
    </div>
  )
}

export default Boards
