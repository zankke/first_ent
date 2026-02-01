import React, { useState } from 'react';

interface CodeViewerProps {
  sqlQuery: string;
  pythonScript: string;
}

const CodeViewer: React.FC<CodeViewerProps> = ({ sqlQuery, pythonScript }) => {
  const [activeTab, setActiveTab] = useState<'sql' | 'python'>('sql');
  const [copied, setCopied] = useState(false);

  const handleCopy = () => {
    const text = activeTab === 'sql' ? sqlQuery : pythonScript;
    navigator.clipboard.writeText(text);
    setCopied(true);
    setTimeout(() => setCopied(false), 2000);
  };

  const handleDownload = () => {
    const text = activeTab === 'sql' ? sqlQuery : pythonScript;
    const extension = activeTab === 'sql' ? 'sql' : 'py';
    const blob = new Blob([text], { type: 'text/plain' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = `artist_query.${extension}`;
    a.click();
    URL.revokeObjectURL(url);
  };

  // Basic syntax highlighting logic for display
  const highlightCode = (code: string, type: 'sql' | 'python') => {
    if (!code) return null;
    if (type === 'sql') {
      return code.split(/(\s+)/).map((word, i) => {
        const upper = word.toUpperCase();
        const keywords = ['INSERT', 'INTO', 'UPDATE', 'SET', 'WHERE', 'VALUES', 'SELECT', 'FROM', 'AND', 'OR', 'NULL'];
        if (keywords.includes(upper)) {
          return <span key={i} className="text-pink-400 font-bold">{word}</span>;
        }
        if (word.startsWith("'") || word.endsWith("'")) {
          return <span key={i} className="text-yellow-200">{word}</span>;
        }
        if (!isNaN(Number(word.replace(',', '')))) {
          return <span key={i} className="text-orange-400">{word}</span>;
        }
        return word;
      });
    } else {
      return code.split(/(\s+)/).map((word, i) => {
        const keywords = ['import', 'from', 'def', 'return', 'if', 'else', 'elif', 'for', 'in', 'while', 'try', 'except', 'as', 'with', 'class'];
        if (keywords.includes(word)) {
          return <span key={i} className="text-blue-400 font-bold">{word}</span>;
        }
        if (word.startsWith('"') || word.startsWith("'")) {
          return <span key={i} className="text-green-300">{word}</span>;
        }
        return word;
      });
    }
  };

  return (
    <div className="bg-slate-950 rounded-2xl border border-white/5 flex flex-col h-full shadow-2xl overflow-hidden glass">
      <div className="flex items-center justify-between px-6 py-4 bg-white/5 border-b border-white/5">
        <div className="flex bg-black/40 p-1 rounded-xl border border-white/10">
          <button
            onClick={() => setActiveTab('sql')}
            className={`px-6 py-2 text-xs font-bold rounded-lg transition-all duration-200 ${
              activeTab === 'sql' 
                ? 'bg-primary text-primary-foreground shadow-lg scale-105' 
                : 'text-muted-foreground hover:text-foreground'
            }`}
          >
            SQL INSERT/UPDATE
          </button>
          {/* Python tab hidden per user request
          <button
            onClick={() => setActiveTab('python')}
            className={`px-6 py-2 text-xs font-bold rounded-lg transition-all duration-200 ${
              activeTab === 'python' 
                ? 'bg-emerald-600 text-white shadow-lg scale-105' 
                : 'text-muted-foreground hover:text-foreground'
            }`}
          >
            PYTHON
          </button>
          */}
        </div>
        
        <div className="flex items-center gap-4">
          <button
            onClick={handleDownload}
            className="text-xs flex items-center gap-1.5 text-muted-foreground hover:text-primary transition-colors"
            title="Download file"
          >
            <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
              <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4" />
            </svg>
            Export
          </button>
          <button
            onClick={handleCopy}
            className="text-xs flex items-center gap-1.5 text-muted-foreground hover:text-white transition-colors min-w-[70px]"
          >
            {copied ? (
              <span className="text-green-400 flex items-center gap-1 font-bold">
                <svg className="h-3 w-3" fill="currentColor" viewBox="0 0 20 20"><path d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z"/></svg>
                Copied
              </span>
            ) : (
              <>
                <svg xmlns="http://www.w3.org/2000/svg" className="h-4 w-4" fill="none" viewBox="0 0 24 24" stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" strokeWidth={2} d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z" />
                </svg>
                Copy
              </>
            )}
          </button>
        </div>
      </div>
      
      <div className="relative flex-1 overflow-hidden bg-black/40">
        <div className="absolute inset-0 overflow-auto p-8 selection:bg-primary/30">
          <pre className="font-mono text-sm leading-relaxed whitespace-pre-wrap break-all">
            <code className="text-slate-300">
              {highlightCode(activeTab === 'sql' ? sqlQuery : pythonScript, activeTab)}
            </code>
          </pre>
        </div>
      </div>
      
      <div className="px-6 py-3 bg-white/5 border-t border-white/5 text-[10px] text-muted-foreground flex justify-between uppercase tracking-widest font-bold">
        <span>{activeTab === 'sql' ? 'MySQL Database Query' : 'Python Automation Script'}</span>
        <span>UTF-8 • JSON PARSED</span>
      </div>
    </div>
  );
};

export default CodeViewer;
