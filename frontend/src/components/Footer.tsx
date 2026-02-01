import React from 'react';

const Footer: React.FC = () => {
  return (
    <footer className="py-6 text-center text-muted-foreground text-sm border-t border-white/5 bg-slate-900/50 backdrop-blur-sm">
      <div className="container mx-auto px-4">
        <p>
          Copyrights &copy;2026{' '}, Developed by{' '}
          <a 
            href="https://theprojectcompany.kr/" 
            target="_blank" 
            rel="noopener noreferrer"
            className="hover:text-primary transition-colors font-medium"
          >
            <em className="text-orange-500">theProjectCompany inc.</em>
          </a>{' '}
          All Rights resereved
        </p>
      </div>
    </footer>
  );
};

export default Footer;