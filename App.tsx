import React, { useState } from 'react';
import { SearchResult, LoadingState } from './types';
import { searchArtist } from './services/geminiService';
import SearchInput from './components/SearchInput';
import ProfileCard from './components/ProfileCard';
import CodeViewer from './components/CodeViewer';

const App: React.FC = () => {
  const [result, setResult] = useState<SearchResult | null>(null);
  const [loading, setLoading] = useState<LoadingState>({ status: 'idle', message: '' });

  const handleSearch = async (term: string, isUpdate: boolean) => {
    setLoading({ status: 'searching', message: `Retrieving information for ${term}...` });
    setResult(null);

    try {
      // Removed the 1.5s artificial timeout to get results as fast as possible
      const data = await searchArtist(term, isUpdate);
      
      setResult(data);
      setLoading({ status: 'complete', message: 'Done!' });
    } catch (error) {
      console.error(error);
      const errorMessage = error instanceof Error ? error.message : 'Failed to retrieve artist information. Please try again.';
      setLoading({ status: 'error', message: errorMessage });
    }
  };

  return (
    <div className="min-h-screen bg-gray-950 text-gray-100 flex flex-col font-sans">
      
      {/* Header */}
      <header className="border-b border-gray-800 bg-gray-900 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 py-4 sm:px-6 lg:px-8 flex justify-between items-center">
          <div className="flex items-center gap-3">
            <div className="p-2 bg-blue-600 rounded-lg shadow-lg shadow-blue-900/50">
               <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-white" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                 <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M19.428 15.428a2 2 0 00-1.022-.547l-2.384-.477a6 6 0 00-3.86.517l-.318.158a6 6 0 01-3.86.517L6.05 15.21a2 2 0 00-1.806.547M8 4h8l-1 1v5.172a2 2 0 00.586 1.414l5 5c1.26 1.26.367 3.414-1.415 3.414H4.828c-1.782 0-2.674-2.154-1.414-3.414l5-5A2 2 0 009 10.172V5L8 4z" />
               </svg>
            </div>
            <h1 className="text-2xl font-bold tracking-tight text-white">
              Artist<span className="text-blue-500">DB</span> Assistant
            </h1>
          </div>
          <div className="text-sm text-gray-500">
            Internal Ent. Tool v1.0
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="flex-1 max-w-7xl w-full mx-auto px-4 py-10 sm:px-6 lg:px-8 flex flex-col">
        
        {/* Search Section */}
        <section className="mb-12 text-center">
          <h2 className="text-3xl font-extrabold text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-indigo-400 mb-4">
            Search Artist & Generate SQL
          </h2>
          <p className="text-gray-400 mb-8 max-w-2xl mx-auto">
            Instantly retrieve Korean artist profiles, analyze Wikipedia data, and generate ready-to-execute SQL INSERT/UPDATE statements and Python automation scripts.
          </p>
          <SearchInput onSearch={handleSearch} isLoading={loading.status !== 'idle' && loading.status !== 'complete' && loading.status !== 'error'} />
          
          {loading.status === 'error' && (
            <div className="mt-6 p-4 bg-red-900/20 border border-red-800 text-red-200 rounded-lg max-w-2xl mx-auto flex items-start gap-3 text-left">
              <svg xmlns="http://www.w3.org/2000/svg" className="h-6 w-6 text-red-500 flex-shrink-0" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z" />
              </svg>
              <div>
                <h3 className="font-semibold text-red-100">Search Failed</h3>
                <p className="text-sm opacity-90 mt-1">{loading.message}</p>
              </div>
            </div>
          )}
        </section>

        {/* Results Section */}
        {result && (
          <section className="grid grid-cols-1 lg:grid-cols-2 gap-8 animate-fade-in-up">
            
            {/* Left Col: Profile & Sources */}
            <div className="space-y-6">
              <ProfileCard profile={result.profile} />
              
              {result.sources.length > 0 && (
                <div className="bg-gray-900 rounded-lg border border-gray-800 p-4">
                  <h4 className="text-sm font-semibold text-gray-400 mb-3 uppercase tracking-wider">Sources Found</h4>
                  <ul className="space-y-2">
                    {result.sources.map((source, idx) => (
                      <li key={idx}>
                        <a 
                          href={source.uri} 
                          target="_blank" 
                          rel="noreferrer"
                          className="text-sm text-blue-400 hover:text-blue-300 hover:underline flex items-center truncate"
                        >
                          <span className="w-1.5 h-1.5 bg-blue-500 rounded-full mr-2 flex-shrink-0"></span>
                          {source.title || source.uri}
                        </a>
                      </li>
                    ))}
                  </ul>
                </div>
              )}
            </div>

            {/* Right Col: Code Output */}
            <div className="h-[600px] lg:h-auto">
              <CodeViewer sqlQuery={result.sqlQuery} pythonScript={result.pythonScript} />
            </div>

          </section>
        )}

        {/* Empty State / Loading Placeholder */}
        {!result && loading.status !== 'error' && (
          <div className="flex-1 flex flex-col items-center justify-center opacity-50 min-h-[300px]">
             {loading.status !== 'idle' ? (
                <div className="flex flex-col items-center">
                  <div className="w-16 h-16 border-4 border-blue-600 border-t-transparent rounded-full animate-spin mb-4"></div>
                  <p className="text-lg text-blue-300 font-medium animate-pulse">{loading.message}</p>
                </div>
             ) : (
                <div className="text-center">
                   <div className="inline-block p-4 rounded-full bg-gray-800 mb-4">
                     <svg xmlns="http://www.w3.org/2000/svg" className="h-10 w-10 text-gray-600" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                       <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={1.5} d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z" />
                     </svg>
                   </div>
                   <p className="text-gray-500">Ready to search. Enter an artist name above.</p>
                </div>
             )}
          </div>
        )}

      </main>
    </div>
  );
};

export default App;