import { useState, useContext } from 'react';
import { 
  Calendar, 
  User, 
  Building, 
  Ruler, 
  Activity, 
  FileText, 
  Shield, 
  ExternalLink, 
  CheckCircle,
  Clock,
  Search
} from 'lucide-react';
import { AuthContext } from '../context/AuthContext';
import CodeViewer from '../components/CodeViewer';

const SearchArtistPage = () => {
  const authContext = useContext(AuthContext);
  const session = authContext?.session;

  const [artistName, setArtistName] = useState('');
  const [sqlQuery, setSqlQuery] = useState('');
  const [pythonScript, setPythonScript] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [artistData, setArtistData] = useState<any>(null);
  const [artistExists, setArtistExists] = useState<boolean>(false);
  const [sources, setSources] = useState<any[]>([]);
  const [wordcloudImage, setWordcloudImage] = useState<string | null>(null);
  const [topKeywords, setTopKeywords] = useState<string[]>([]);
  const [applyLoading, setApplyLoading] = useState(false);
  const [applyError, setApplyError] = useState('');

  const handleSearch = async () => {
    setLoading(true);
    setError('');
    setSqlQuery('');
    setPythonScript('');
    setArtistData(null);
    setArtistExists(false);
    setSources([]);
    setWordcloudImage(null);
    setTopKeywords([]);

    try {
      const response = await fetch(`/api/artists/search_and_generate_sql?artist_name=${encodeURIComponent(artistName)}`);
      
      const contentType = response.headers.get("content-type");
      if (contentType && contentType.indexOf("application/json") !== -1) {
        const data = await response.json();
        if (!response.ok) {
          throw new Error(data.error || '아티스트 정보를 가져오는데 실패했습니다.');
        }
        setSqlQuery(data.sql_query);
        setPythonScript(data.python_script || '');
        setArtistData(data.artist_data);
        setArtistExists(data.artist_exists);
        setSources(data.sources || []);
        setWordcloudImage(data.wordcloud_image);
        setTopKeywords(data.top_keywords || []);
      } else {
        const text = await response.text();
        console.error("Non-JSON response received:", text);
        throw new Error(`서버 오류가 발생했습니다 (Status: ${response.status}). 관리자에게 문의하세요.`);
      }
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleApplyToDB = async () => {
    if (!artistData) {
      setApplyError('아티스트 데이터가 없습니다.');
      return;
    }

    setApplyLoading(true);
    setApplyError('');

    try {
      const response = await fetch('/api/artists/upsert-from-wiki', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
          'Authorization': `Bearer ${session?.access_token}`
        },
        body: JSON.stringify({ artist_data: artistData, artist_exists: artistExists }),
      });

      const contentType = response.headers.get("content-type");
      if (contentType && contentType.indexOf("application/json") !== -1) {
        const data = await response.json();
        if (!response.ok) {
          throw new Error(data.error || 'DB 적용에 실패했습니다.');
        }
        alert(data.message || '아티스트 정보가 DB에 성공적으로 적용되었습니다.');
      } else {
        const text = await response.text();
        console.error("Non-JSON response received:", text);
        throw new Error(`DB 적용 중 서버 오류가 발생했습니다 (Status: ${response.status}).`);
      }
    } catch (err: any) {
      setApplyError(err.message);
    } finally {
      setApplyLoading(false);
    }
  };

  const InfoItem = ({ icon: Icon, label, value }: { icon: any, label: string, value: any }) => {
    const displayValue = (value !== null && value !== undefined && value !== '') ? String(value) : 'N/A';
    return (
      <div className="flex flex-col space-y-1">
        <span className="text-[10px] font-bold text-muted-foreground uppercase tracking-widest flex items-center gap-1">
          <Icon className="w-3 h-3" />
          {label}
        </span>
        <div className="flex items-center gap-3">
          <div className="w-0.5 h-6 bg-primary/30 rounded-full" />
          <span className="text-sm font-medium text-foreground">{displayValue}</span>
        </div>
      </div>
    );
  };

  return (
    <div className="p-6 max-w-5xl mx-auto space-y-8">
      <div className="flex items-center justify-between">
        <div>
          <h1 className="text-4xl font-bold gradient-text mb-2 tracking-tight flex items-center gap-2">
            <span>
              <svg xmlns="http://www.w3.org/2000/svg" className="inline-block w-8 h-8 text-primary" viewBox="0 0 24 24" fill="none">
                <circle cx="12" cy="8" r="4" fill="currentColor" />
                <path d="M3 20c0-3.866 3.582-7 9-7s9 3.134 9 7" fill="currentColor" opacity="0.15"/>
                <path d="M3 20c0-3.866 3.582-7 9-7s9 3.134 9 7" stroke="currentColor" strokeWidth="1.5" strokeLinecap="round"/>
              </svg>
            </span>
            [ AI ] 아티스트 검색 
          </h1>
          <p className="text-muted-foreground">'아티스트'를 검색하고 DB에 Update &rarr; 검색 결과(Google SERP, WIKIPEDIA, SRIBD,YTB)로부터 데이터 추출</p>
        </div>
      </div>

      <div className="glass rounded-3xl p-8 shadow-2xl border-white/5 space-y-6">
        <div className="flex gap-4">
          <div className="relative flex-1">
            <Search className="absolute left-4 top-1/2 -translate-y-1/2 text-muted-foreground w-5 h-5" />
            <input
              type="text"
              className="w-full pl-12 pr-4 py-4 bg-background/50 border border-white/10 rounded-2xl focus:outline-none focus:ring-2 focus:ring-primary/50 text-lg transition-all"
              value={artistName}
              onChange={(e) => setArtistName(e.target.value)}
              onKeyDown={(e) => e.key === 'Enter' && handleSearch()}
              placeholder="아티스트 이름을 입력하세요 (예: 아이유, 탁재훈)"
              disabled={loading}
            />
          </div>
          <button
            onClick={handleSearch}
            className="px-8 py-4 bg-primary text-primary-foreground font-bold rounded-2xl hover:scale-[1.02] active:scale-[0.98] transition-all disabled:opacity-50 flex items-center gap-2 shadow-lg shadow-primary/25"
            disabled={loading}
          >
            {loading ? <Activity className="w-5 h-5 animate-spin" /> : <ExternalLink className="w-5 h-5" />}
            {loading ? '검색 중...' : '검색 및 분석'}
          </button>
        </div>

        {error && (
          <div className="p-4 bg-destructive/10 border border-destructive/20 text-destructive rounded-2xl flex items-center gap-3">
            <div className="w-2 h-2 rounded-full bg-destructive animate-pulse" />
            <span className="font-medium">{error}</span>
          </div>
        )}
      </div>

      {artistData && (
        <div className="animate-in fade-in slide-in-from-bottom-4 duration-700 space-y-12">
          {/* Profile Card */}
          <div className="glass rounded-[2.5rem] overflow-hidden border-white/10 shadow-2xl bg-gradient-to-br from-slate-900/95 to-slate-950/95 backdrop-blur-3xl ring-1 ring-white/5 mb-8">
            <div className="p-10 space-y-10">
              {/* Header */}
              <div className="flex items-center gap-8 pb-8 border-b border-white/5">
                <div className="w-24 h-24 rounded-full bg-gradient-to-br from-slate-700 to-slate-800 flex items-center justify-center text-3xl font-bold text-white shadow-xl ring-4 ring-white/5">
                  {artistData.name?.charAt(0)}
                </div>
                <div className="flex-1 space-y-2">
                  <div className="flex items-center gap-3">
                    <h2 className="text-4xl font-bold text-white tracking-tight">{artistData.name}</h2>
                    <span className="px-3 py-1 bg-primary/20 text-primary text-xs font-bold rounded-full border border-primary/20 uppercase tracking-widest">
                      {artistData.nationality?.includes('한국') ? 'KR' : artistData.nationality || 'INTL'}
                    </span>
                  </div>
                  <div className="flex items-center gap-4 text-muted-foreground font-medium">
                    <span className="text-lg">{artistData.eng_name}</span>
                    <div className="w-1 h-1 rounded-full bg-white/20" />
                    <span className="text-sm px-3 py-1 bg-white/5 rounded-lg border border-white/5">
                      {artistData.genre || 'K-POP, BALLAD'}
                    </span>
                  </div>
                </div>
              </div>

              {/* Stats Grid */}
              <div className="grid grid-cols-2 gap-y-10 gap-x-8">
                <InfoItem icon={Calendar} label="Birth Date" value={artistData.birth_date} />
                <InfoItem icon={CheckCircle} label="Debut" value={artistData.debut_date} />
                <InfoItem icon={Building} label="Agency" value={artistData.current_agency_name} />
                <InfoItem icon={Ruler} label="Height" value={artistData.height_cm ? `${artistData.height_cm} cm` : 'N/A'} />
                <InfoItem icon={User} label="Gender" value={artistData.gender} />
                <InfoItem icon={Shield} label="Status" value={artistData.status || 'ACTIVE'} />
                <InfoItem icon={Activity} label="Recent Drama/Movie" value={artistData.recent_activity_name} />
                <InfoItem icon={Clock} label="Recent Activity Category" value={artistData.recent_activity_category} />
              </div>

              {/* Biography Section */}
              <div className="pt-10 border-t border-white/10 space-y-5">
                <div className="flex items-center gap-3 text-primary">
                  <div className="p-2 bg-primary/10 rounded-lg">
                    <FileText className="w-5 h-5" />
                  </div>
                  <span className="text-sm font-bold uppercase tracking-[0.2em]">Biography Summary</span>
                </div>
                <div className="p-8 bg-white/5 rounded-[2rem] border border-white/10 leading-relaxed text-slate-300 font-light text-base shadow-inner">
                  {artistData.wiki_summary}
                </div>
              </div>

                              {/* Sources Section */}
                              {sources && sources.length > 0 && (
                                <div className="pt-10 border-t border-white/10 space-y-5">
                                  <div className="flex items-center justify-between">
                                    <div className="flex items-center gap-3 text-primary">
                                      <div className="p-2 bg-primary/10 rounded-lg">
                                        <ExternalLink className="w-5 h-5" />
                                      </div>
                                      <span className="text-sm font-bold uppercase tracking-[0.2em]">Sources Found</span>
                                    </div>
                                    <span className="text-[10px] text-muted-foreground font-medium uppercase tracking-wider bg-white/5 px-3 py-1 rounded-full border border-white/5">
                                      {sources.length} references
                                    </span>
                                  </div>
                                  
                                  <div className="grid grid-cols-1 gap-4">
                                    {sources.map((source: any, idx: number) => (
                                      <a 
                                        key={idx}
                                        href={source.uri} 
                                        target="_blank" 
                                        rel="noreferrer"
                                        className="group glass p-4 rounded-2xl border border-white/5 hover:border-primary/30 transition-all duration-300 flex items-center gap-5 hover:bg-white/5"
                                      >
                                        {/* Thumbnail / Favicon */}
                                        <div className="w-12 h-12 rounded-xl bg-white/5 flex-shrink-0 overflow-hidden border border-white/10 group-hover:scale-110 transition-transform">
                                          <img 
                                            src={source.thumbnail || `https://www.google.com/s2/favicons?domain=${source.source}&sz=64`} 
                                            alt={source.source}
                                            className="w-full h-full object-cover p-2 opacity-80 group-hover:opacity-100 transition-opacity"
                                            onError={(e: any) => { e.target.src = 'https://www.google.com/s2/favicons?domain=google.com&sz=64'; }}
                                          />
                                        </div>
              
                                        {/* Source Info */}
                                        <div className="flex-1 min-w-0 space-y-1">
                                          <div className="flex items-center gap-3">
                                            <span className="text-[10px] font-bold text-primary uppercase tracking-widest px-2 py-0.5 bg-primary/10 rounded-md border border-primary/10">
                                              {source.source || 'WEB'}
                                            </span>
                                            <span className="text-[10px] text-muted-foreground flex items-center gap-1.5">
                                              <Clock className="w-3 h-3" />
                                              {source.search_date}
                                            </span>
                                          </div>
                                          <h4 className="text-sm font-semibold text-white/90 truncate group-hover:text-primary transition-colors">
                                            {source.title}
                                          </h4>
                                          <p className="text-[11px] text-muted-foreground truncate opacity-60">
                                            {source.uri}
                                          </p>
                                        </div>
              
                                        <div className="flex-shrink-0 opacity-0 group-hover:opacity-100 transition-opacity pr-2">
                                          <ExternalLink className="w-4 h-4 text-primary" />
                                        </div>
                                      </a>
                                    ))}
                                  </div>
                                </div>
                              )}
              {/* Wordcloud Section */}
              {wordcloudImage && (
                <div className="pt-10 border-t border-white/10 space-y-5">
                   <div className="flex items-center gap-3 text-primary">
                      <div className="p-2 bg-primary/10 rounded-lg">
                        <Activity className="w-5 h-5" />
                      </div>
                      <span className="text-sm font-bold uppercase tracking-[0.2em]">Keyword Analysis</span>
                    </div>
                    <div className="p-6 bg-white/5 rounded-[2rem] border border-white/10 shadow-inner flex flex-col items-center">
                      <img 
                        src={wordcloudImage} 
                        alt="Keyword Wordcloud" 
                        className="w-[85%] max-w-5xl h-auto rounded-xl shadow-lg border border-white/5"
                        style={{ width: "85%" }}
                      />
                      
                      {topKeywords.length > 0 && (
                        <div className="mt-6 flex flex-wrap gap-2 justify-center">
                          {topKeywords.map((keyword, idx) => (
                            <span key={idx} className="px-3 py-1 bg-white/10 text-white/80 text-xs rounded-full border border-white/5">
                              #{keyword}
                            </span>
                          ))}
                        </div>
                      )}
                    </div>
                </div>
              )}
            </div>
          </div>

          {/* Apply Button Section */}
          <div className="glass rounded-[2rem] p-8 border-white/10 flex flex-col gap-6 bg-gradient-to-br from-slate-900/50 to-slate-950/50">
            <div className="flex flex-col sm:flex-row items-center justify-between gap-6 mb-3">
              <div className="flex flex-col gap-1">
                <span className="text-[10px] font-bold text-muted-foreground uppercase tracking-[0.2em]">Sync Status</span>
                <span className={`text-xs px-4 py-1.5 rounded-full font-bold border ${artistExists ? 'bg-orange-500/10 text-orange-500 border-orange-500/20' : 'bg-green-500/10 text-green-500 border-green-500/20'}`}>
                  {artistExists ? 'EXISTING ARTIST - UPDATE MODE' : 'NEW ARTIST - INSERT MODE'}
                </span>
              </div>
              <button
                onClick={handleApplyToDB}
                className="w-full sm:w-auto px-10 py-5 bg-green-500 text-white font-bold rounded-2xl hover:bg-green-600 hover:scale-[1.02] transition-all flex items-center justify-center gap-3 shadow-2xl shadow-green-500/20 active:scale-95 disabled:opacity-50"
                disabled={applyLoading}
              >
                {applyLoading ? <Activity className="w-6 h-6 animate-spin" /> : <CheckCircle className="w-6 h-6" />}
                <span className="text-lg">{applyLoading ? 'Applying...' : 'Update Database'}</span>
              </button>
            </div>
            {applyError && (
              <div className="p-4 bg-destructive/10 border border-destructive/20 text-destructive rounded-xl text-sm font-medium">
                {applyError}
              </div>
            )}
          </div>

          {/* Code Viewer */}
          <div className="mb-8">
            <CodeViewer sqlQuery={sqlQuery} pythonScript={pythonScript} />
          </div>

        </div>
      )}
    </div>
  );
};

export default SearchArtistPage;
