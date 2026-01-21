import React, { useState } from 'react';

const SearchArtistPage = () => {
  const [artistName, setArtistName] = useState('');
  const [sqlQuery, setSqlQuery] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');
  const [artistData, setArtistData] = useState<any>(null); // New state for artist data
  const [artistExists, setArtistExists] = useState<boolean>(false); // New state for artist existence
  const [applyLoading, setApplyLoading] = useState(false); // New state for apply to DB loading
  const [applyError, setApplyError] = useState(''); // New state for apply to DB error

  const handleSearch = async () => {
    setLoading(true);
    setError('');
    setSqlQuery('');
    setArtistData(null); // Clear previous artist data
    setArtistExists(false); // Clear previous existence flag

    try {
      const response = await fetch(`/api/artists/search_and_generate_sql?artist_name=${encodeURIComponent(artistName)}`);
      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'Failed to fetch artist data.');
      }

      setSqlQuery(data.sql_query);
      setArtistData(data.artist_data); // Store the raw artist data
      setArtistExists(data.artist_exists); // Store the existence flag
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
        },
        body: JSON.stringify({ artist_data: artistData, artist_exists: artistExists }),
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || 'DB 적용에 실패했습니다.');
      }

      alert(data.message || '아티스트 정보가 DB에 성공적으로 적용되었습니다.');
      // Optionally, re-fetch artists or update UI after successful application
      // if this page is part of a larger artist management view
    } catch (err: any) {
      setApplyError(err.message);
    } finally {
      setApplyLoading(false);
    }
  };

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6 text-white">아티스트 검색 및 SQL 생성</h1>
      <div className="bg-gray-800 rounded-xl p-6 shadow-lg">
        <div className="mb-4">
          <label htmlFor="artistName" className="block text-gray-300 text-sm font-medium mb-2">
            아티스트 이름:
          </label>
          <input
            type="text"
            id="artistName"
            className="w-full px-4 py-2 rounded-lg bg-gray-700 text-white border border-gray-600 focus:outline-none focus:ring-2 focus:ring-purple-500"
            value={artistName}
            onChange={(e) => setArtistName(e.target.value)}
            placeholder="아티스트 이름을 입력하세요 (예: 아이유)"
            disabled={loading}
          />
        </div>
        <button
          onClick={handleSearch}
          className="bg-purple-600 hover:bg-purple-700 text-white font-bold py-2 px-4 rounded-lg transition-colors duration-200"
          disabled={loading}
        >
          {loading ? '검색 중...' : '검색 및 SQL 생성'}
        </button>

        {error && (
          <div className="mt-4 p-3 bg-red-600 text-white rounded-lg">
            Error: {error}
          </div>
        )}

        {sqlQuery && (
          <div className="mt-6">
            <h2 className="text-xl font-semibold mb-3 text-white">생성된 SQL 쿼리:</h2>
            <div className="bg-gray-900 p-4 rounded-lg overflow-x-auto">
              <pre className="text-green-400 whitespace-pre-wrap">{sqlQuery}</pre>
            </div>
            <div className="flex space-x-3 mt-3">
              <button
                onClick={() => navigator.clipboard.writeText(sqlQuery)}
                className="bg-blue-600 hover:bg-blue-700 text-white font-bold py-2 px-4 rounded-lg transition-colors duration-200"
              >
                SQL 복사
              </button>
              {artistData && (
                <button
                  onClick={handleApplyToDB}
                  className="bg-green-600 hover:bg-green-700 text-white font-bold py-2 px-4 rounded-lg transition-colors duration-200"
                  disabled={applyLoading}
                >
                  {applyLoading ? '적용 중...' : 'DB에 적용'}
                </button>
              )}
            </div>
            {applyError && (
              <div className="mt-4 p-3 bg-red-600 text-white rounded-lg">
                Error: {applyError}
              </div>
            )}
          </div>
        )}

      </div>
    </div>
  );
};

export default SearchArtistPage;
