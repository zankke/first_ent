import React, { useState, useEffect } from 'react'
import { useLocation } from 'react-router-dom'
import { Plus, Search, Filter, MoreVertical, Edit, Trash2, Eye } from 'lucide-react'
import ArtistForm from '../components/ArtistForm'
import Pagination from '../components/Pagination' // Import Pagination component

interface Artist {
  id: number;
  name: string;
  birth_date: string;
  height_cm: number;
  debut_date: string;
  genre: string;
  agency_id: number;
  nationality: string;
  is_korean: boolean;
  gender: 'WOMAN' | 'MEN' | 'EXTRA' | 'FOREIGN';
  status: string;
  category_id: number;
  platform: string;
  social_media_url: string;
  profile_photo: string;
  guarantee_krw: number; // New field
}

const Artists = () => {
  const [artists, setArtists] = useState([])
  const [isModalOpen, setIsModalOpen] = useState(false)
  const [selectedArtist, setSelectedArtist] = useState(null)
  const [selectedArtistIds, setSelectedArtistIds] = useState<number[]>([])
  const [reportFormat, setReportFormat] = useState<'pdf' | 'pptx'>('pdf')
  const [isLoading, setIsLoading] = useState(true)
  const [error, setError] = useState(null)
  const [searchQuery, setSearchQuery] = useState('')
  const [filterStatus, setFilterStatus] = useState('')
  const [filterGender, setFilterGender] = useState('')
  const [filterNationality, setFilterNationality] = useState('')
  const [filterGenre, setFilterGenre] = useState('') // New state for genre filter
  const [filterCategory, setFilterCategory] = useState('')
  const [isGeneratingReport, setIsGeneratingReport] = useState(false)
  const [currentPage, setCurrentPage] = useState(1) // New state for current page
  const [totalPages, setTotalPages] = useState(1)     // New state for total pages
  const [perPage, setPerPage] = useState(10)           // New state for items per page

  const location = useLocation()

  useEffect(() => {
    const params = new URLSearchParams(location.search)
    const query = params.get('query')
    if (query) {
      setSearchQuery(query)
    }
    fetchArtists()
  }, [location.search, filterStatus, filterGender, filterNationality, filterCategory, filterGenre, currentPage, perPage]) // Add currentPage and perPage to dependencies

  const fetchArtists = async () => {
    setIsLoading(true)
    setError(null)
    try {
      const params = new URLSearchParams()
      if (searchQuery) params.append('query', searchQuery)
      if (filterStatus) params.append('status', filterStatus)
      if (filterGender) params.append('gender', filterGender)
      if (filterNationality) params.append('nationality', filterNationality)
      if (filterGenre) params.append('genre', filterGenre)
      if (filterCategory) params.append('category_id', filterCategory)
      params.append('page', currentPage.toString()) // Add page parameter
      params.append('per_page', perPage.toString()) // Add per_page parameter

      const response = await fetch(`/api/artists/?${params.toString()}`)
      if (!response.ok) {
        throw new Error('Network response was not ok')
      }
      const data = await response.json()
      setArtists(data.artists)
      setTotalPages(data.pages) // Update total pages from backend response
    } catch (error) {
      console.error('Error fetching artists:', error)
      setError('아티스트 DB를 불러오는 데 실패했습니다.')
    } finally {
      setIsLoading(false)
    }
  }

  const handlePageChange = (page: number) => {
    setCurrentPage(page)
  }

  const handleAddArtist = () => {
    setSelectedArtist(null)
    setIsModalOpen(true)
  }

  const handleEditArtist = (artist) => {
    setSelectedArtist(artist)
    setIsModalOpen(true)
  }

  const handleCloseModal = () => {
    setIsModalOpen(false)
    setSelectedArtist(null)
  }

  const handleArtistAdded = () => {
    fetchArtists()
  }

  const handleSelectArtist = (artistId: number) => {
    console.log("DEBUG: handleSelectArtist - artistId:", artistId);
    setSelectedArtistIds((prevSelected) => {
      console.log("DEBUG: handleSelectArtist - prevSelected:", prevSelected);
      const newSelected = prevSelected.includes(artistId)
        ? prevSelected.filter((id) => id !== artistId)
        : [...prevSelected, artistId];
      console.log("DEBUG: handleSelectArtist - newSelected:", newSelected);
      return newSelected;
    });
  }

  const handleGenerateReport = async () => {
    if (selectedArtistIds.length === 0) {
      alert('Please select at least one artist to generate a report.')
      return
    }

    setIsGeneratingReport(true) // Show loading indicator
    console.log("DEBUG: Sending artist_ids for report:", selectedArtistIds);

    try {
      const response = await fetch('/api/artists/report/', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          artist_ids: selectedArtistIds,
          report_format: reportFormat,
        }),
      })

      if (!response.ok) {
        throw new Error('Report generation failed')
      }

      const blob = await response.blob()
      const url = window.URL.createObjectURL(blob)
      const a = document.createElement('a')
      a.href = url
      a.download = `artists_report.${reportFormat}`
      document.body.appendChild(a)
      a.click()
      a.remove()
      window.URL.revokeObjectURL(url)

      alert('Report generated and downloaded successfully!')
    } catch (error) {
      console.error('Error generating report:', error)
      alert('Failed to generate report.')
    } finally {
      setIsGeneratingReport(false) // Hide loading indicator
    }
  }

  const handleDeleteArtist = async (artistId) => {
    if (window.confirm('Are you sure you want to delete this artist?')) {
      try {
        const response = await fetch(`/api/artists/${artistId}`, {
          method: 'DELETE',
        })

        if (!response.ok) {
          throw new Error('Network response was not ok')
        }

        fetchArtists()
      } catch (error) {
        console.error('Error deleting artist:', error)
      }
    }
  }

  const handleSearchNews = async (artistName: string, artistId: number) => {
    const googleNewsUrl = `https://www.google.com/search?q=${encodeURIComponent(artistName)}&tbm=nws`;
    window.open(googleNewsUrl, '_blank');

    try {
      const response = await fetch('/api/news/crawl', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({ artist_id: artistId }),
      });

      if (!response.ok) {
        throw new Error('Failed to trigger news crawl');
      }

      const data = await response.json();
      alert(data.message);
    } catch (error) {
      console.error('Error triggering news crawl:', error);
      alert('Failed to trigger news crawl.');
    }
  };

  return (
    <div className="space-y-6">
      {isGeneratingReport && (
        <div className="fixed inset-0 bg-black bg-opacity-50 flex items-center justify-center z-50">
          <div className="bg-white p-6 rounded-lg shadow-lg flex items-center space-x-3">
            <svg className="animate-spin h-10 w-10 text-orange-500" xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24">
              <circle className="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" strokeWidth="4"></circle>
              <path className="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4zm2 5.291A7.962 7.962 0 014 12H0c0 3.042 1.135 5.824 3 7.938l3-2.647z"></path>
            </svg>
            <p className="text-gray-700">리포트 생성 중...</p>
          </div>
        </div>
      )}
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-3xl font-bold gradient-text mb-2">아티스트 관리</h1>
          <p className="text-muted-foreground">등록된 아티스트를 관리하고 모니터링하세요</p>
        </div>
        <div className="flex items-center space-x-4">
          <button 
            onClick={handleAddArtist}
            className="flex items-center space-x-2 px-4 py-2 text-white rounded-xl hover:bg-orange-600 transition-colors"
            style={{ backgroundColor: 'rgb(237 113 4)' }}
          >
            <Plus className="w-4 h-4" />
            <span>새 아티스트 추가</span>
          </button>
          <button 
            onClick={handleGenerateReport}
            className="flex items-center space-x-2 px-4 py-2 text-white rounded-xl hover:bg-blue-600 transition-colors"
            style={{ backgroundColor: selectedArtistIds.length > 0 ? 'rgb(59 130 246)' : 'rgb(156 163 175)' }}
            disabled={selectedArtistIds.length === 0}
          >
            <span>리포트 생성</span>
          </button>
          <select
            value={reportFormat}
            onChange={(e) => setReportFormat(e.target.value as 'pdf' | 'pptx')}
            className="px-4 py-2 border border-border rounded-xl bg-muted/50 focus:outline-none focus:ring-2 focus:ring-primary/50"
          >
            <option value="pdf">PDF</option>
            <option value="pptx">PPTX</option>
          </select>
        </div>
      </div>
      
      <ArtistForm 
        isOpen={isModalOpen} 
        onClose={handleCloseModal} 
        onArtistAdded={handleArtistAdded}
        artist={selectedArtist}
      />
      
      {/* 검색 및 필터 */}
      <div className="glass rounded-2xl p-6">
        <div className="flex items-center space-x-4">
          <div className="relative flex-1">
            <Search className="absolute left-3 top-1/2 transform -translate-y-1/2 text-muted-foreground w-4 h-4" />
            <input
              type="text"
              placeholder="아티스트 검색... (이름, 국적, 장르)"
              className="w-full pl-10 pr-4 py-2 bg-muted/50 border border-border rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/50"
              value={searchQuery}
              onChange={(e) => setSearchQuery(e.target.value)}
              onKeyPress={(e) => {
                if (e.key === 'Enter') {
                  fetchArtists();
                }
              }}
            />
          </div>

          <select
            value={filterCategory}
            onChange={(e) => setFilterCategory(e.target.value)}
            className="px-4 py-2 bg-muted/50 border border-border rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/50"
          >
            <option value="">모델 카테고리</option>
            <option value="1">일반모델(성인)</option>
            <option value="2">일반모델(아동)</option>
            <option value="3">일반모델(노인)</option>
            <option value="4">패션모델</option>
            <option value="5">배우</option>
            <option value="6">아동모델</option>
            <option value="7">전문 외국인 모델</option>
            <option value="8">Influencer</option>
            <option value="9">Celebrity</option>
            <option value="10">SINGER</option>
          </select>

          <select
            value={filterStatus}
            onChange={(e) => setFilterStatus(e.target.value)}
            className="px-4 py-2 bg-muted/50 border border-border rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/50"
          >
            <option value="">모든 상태</option>
            <option value="ACTIVE">활동중</option>
            <option value="RESTING">휴식중</option>
            <option value="OTHER">기타</option>
          </select>
          <select
            value={filterGender}
            onChange={(e) => setFilterGender(e.target.value)}
            className="px-4 py-2 bg-muted/50 border border-border rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/50"
          >
            <option value="">모든 성별</option>
            <option value="WOMAN">여성</option>
            <option value="MEN">남성</option>
            <option value="EXTRA">기타</option>
          </select>
          <select
            value={filterNationality}
            onChange={(e) => setFilterNationality(e.target.value)}
            className="px-4 py-2 bg-muted/50 border border-border rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/50"
          >
            <option value="">모든 국적</option>
            <option value="KOREAN">내국인</option>
            <option value="FOREIGN">외국인</option>
          </select>
          <select
            value={filterGenre}
            onChange={(e) => setFilterGenre(e.target.value)}
            className="px-4 py-2 bg-muted/50 border border-border rounded-xl focus:outline-none focus:ring-2 focus:ring-primary/50"
          >
            <option value="">모든 장르</option>
            <option value="배우">배우</option>
            <option value="가수">가수</option>
            <option value="모델">모델</option>
            <option value="방송인">방송인</option>
            <option value="배우/방송인">배우/방송인</option>
            <option value="가수/방송인">가수/방송인</option>
            <option value="가수/배우">가수/배우</option>
            <option value="배우/모델">배우/모델</option>
            <option value="드라마, 영화">드라마, 영화</option>
            <option value="ETC">기타</option>
          </select>
          <button
            onClick={fetchArtists}
            className="flex items-center space-x-2 px-4 py-2 text-white rounded-xl hover:bg-orange-600 transition-colors"
            style={{ backgroundColor: 'rgb(237 113 4)' }}
          >
            <Search className="w-4 h-4" />
            <span>검색 및 필터</span>
          </button>
        </div>
      </div>
      
      {/* 아티스트 목록 */}
      <div className="glass rounded-2xl overflow-hidden">
        {isLoading && (
          <div className="p-6 text-center text-gray-400">
            아티스트 목록을 불러오는 중...
          </div>
        )}

        <div className="overflow-x-auto">
          <table className="w-full">
            <thead className="border-b border-border">
              <tr>
                <th className="text-left p-6 font-medium text-muted-foreground">선택</th>
                <th className="text-left p-6 font-medium text-muted-foreground">아티스트</th>
                <th className="text-left p-6 font-medium text-muted-foreground">생년월일</th>
                <th className="text-left p-6 font-medium text-muted-foreground">성별</th>
                <th className="text-left p-6 font-medium text-muted-foreground">상태</th>
                <th className="text-left p-6 font-medium text-muted-foreground">장르</th>
                <th className="text-left p-6 font-medium text-muted-foreground">모델료 (원)</th>
                <th className="text-right p-6 font-medium text-muted-foreground">액션</th>
              </tr>
            </thead>
            <tbody>
              {artists.length > 0 && artists.map((artist) => (
                <tr key={artist.id} className="border-b border-border/50 hover:bg-muted/30 transition-colors">
                  <td className="p-6">
                    <input
                      type="checkbox"
                      checked={selectedArtistIds.includes(artist.id)}
                      onChange={() => handleSelectArtist(artist.id)}
                      className="form-checkbox h-5 w-5 text-orange-600 rounded focus:ring-orange-500"
                    />
                  </td>
                  <td className="p-6">
                    <div className="flex items-center space-x-3">
                      <img 
                        src={artist.profile_photo || "https://via.placeholder.com/150/0000FF/FFFFFF?text=No+Image"} 
                        alt={artist.name} 
                        className="w-12 h-12 object-cover rounded-xl"
                        onError={(e) => {
                          e.currentTarget.src = "https://via.placeholder.com/150/0000FF/FFFFFF?text=No+Image";
                        }}
                      />
                      <div>
                        <p className="font-medium">{artist.name}</p>
                      </div>
                    </div>
                  </td>
                  <td className="p-6">
                    <span className="text-sm">{artist.birth_date}</span>
                  </td>
                  <td className="p-6">
                    <span className="text-sm">{artist.gender}</span>
                  </td>
                  <td className="p-6">
                    <span className="text-sm">{artist.status}</span>
                  </td>
                  <td className="p-6">
                    <span className="text-sm">{artist.genre || 'N/A'}</span>
                  </td>
                  <td className="p-6">
                    <span className="text-sm">{artist.guarantee_krw ? artist.guarantee_krw.toLocaleString() + '원' : 'N/A'}</span>
                  </td>
                  <td className="p-6">
                    <div className="flex items-center justify-end space-x-2">
                      <button onClick={() => handleSearchNews(artist.name, artist.id)} className="p-2 text-muted-foreground hover:text-foreground transition-colors">
                        <Search className="w-4 h-4" />
                      </button>
                      <button className="p-2 text-muted-foreground hover:text-foreground transition-colors">
                        <Eye className="w-4 h-4" />
                      </button>
                      <button onClick={() => handleEditArtist(artist)} className="p-2 text-muted-foreground hover:text-foreground transition-colors">
                        <Edit className="w-4 h-4" />
                      </button>
                      <button onClick={() => handleDeleteArtist(artist.id)} className="p-2 text-muted-foreground hover:text-red-500 transition-colors">
                        <Trash2 className="w-4 h-4" />
                      </button>
                      <button className="p-2 text-muted-foreground hover:text-foreground transition-colors">
                        <MoreVertical className="w-4 h-4" />
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
          {!isLoading && !error && artists.length === 0 && (
            <div className="p-6 text-center text-gray-400">
              등록된 아티스트가 없습니다.
            </div>
          )}
        </div>

        {error && (
          <div className="p-6 text-center text-red-500">
            아티스트 DB를 불러오는 데 실패했습니다.
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
    </div>
  )
}


export default Artists
