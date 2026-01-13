import React from 'react'
import { ChevronLeft, ChevronRight, ChevronsLeft, ChevronsRight } from 'lucide-react'

interface PaginationProps {
  currentPage: number;
  totalPages: number;
  onPageChange: (page: number) => void;
}

const Pagination: React.FC<PaginationProps> = ({
  currentPage,
  totalPages,
  onPageChange,
}) => {
  const pageGroupSize = 10; // Number of pages to display in a group

  const currentGroup = Math.ceil(currentPage / pageGroupSize);
  const startPage = (currentGroup - 1) * pageGroupSize + 1;
  const endPage = Math.min(currentGroup * pageGroupSize, totalPages);

  const pageNumbers = []
  for (let i = startPage; i <= endPage; i++) {
    pageNumbers.push(i)
  }

  const handlePrevGroup = () => {
    onPageChange(startPage - 1);
  };

  const handleNextGroup = () => {
    onPageChange(endPage + 1);
  };

  return (
    <div className="flex items-center justify-center space-x-2 mt-8">
      <button
        onClick={() => onPageChange(1)}
        disabled={currentPage === 1}
        className="px-3 py-2 rounded-xl bg-muted/50 text-muted-foreground hover:bg-muted disabled:opacity-50 transition-colors"
      >
        <ChevronsLeft className="w-4 h-4" />
      </button>
      <button
        onClick={handlePrevGroup}
        disabled={startPage === 1}
        className="px-3 py-2 rounded-xl bg-muted/50 text-muted-foreground hover:bg-muted disabled:opacity-50 transition-colors"
      >
        <ChevronLeft className="w-4 h-4" />
      </button>
      {pageNumbers.map((page) => (
        <button
          key={page}
          onClick={() => onPageChange(page)}
          className={`px-4 py-2 rounded-xl transition-colors ${
            page === currentPage
              ? 'bg-orange-500 text-white'
              : 'bg-muted/50 text-muted-foreground hover:bg-muted'
          }`}
        >
          {page}
        </button>
      ))}
      <button
        onClick={handleNextGroup}
        disabled={endPage === totalPages}
        className="px-3 py-2 rounded-xl bg-muted/50 text-muted-foreground hover:bg-muted disabled:opacity-50 transition-colors"
      >
        <ChevronRight className="w-4 h-4" />
      </button>
      <button
        onClick={() => onPageChange(totalPages)}
        disabled={currentPage === totalPages}
        className="px-3 py-2 rounded-xl bg-muted/50 text-muted-foreground hover:bg-muted disabled:opacity-50 transition-colors"
      >
        <ChevronsRight className="w-4 h-4" />
      </button>
    </div>
  )
}

export default Pagination