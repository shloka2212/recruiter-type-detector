import React from "react";

// --- NEW: Skeleton Loader Component ---
// This will be shown while the API call is in progress
const SkeletonLoader = () => (
  <div className="result-box fade-in">
    <div className="skeleton skeleton-title"></div>
    <div className="skeleton skeleton-text"></div>
    <div className="skeleton skeleton-text"></div>
    <div className="skeleton skeleton-text short"></div>
  </div>
);


function ResultCard({ result, loading }) {
  // --- UPDATED: Show SkeletonLoader when loading ---
  if (loading) {
    return <SkeletonLoader />;
  }

  // Show nothing if there's no result or loading is finished
  if (!result) {
    return null;
  }

  // --- UPDATED: Error display now uses CSS classes instead of inline styles ---
  if (result.status === "error") {
    return (
      <div className="result-box fade-in error">
        <h3>Error</h3>
        <p>{result.explanation}</p>
      </div>
    );
  }

  // --- UPDATED: Cleaner class name logic ---
  const statusClass = `status ${result.status}`;

  return (
    <div className="result-box fade-in">
      <div className="result-header">
        <h3>Status</h3>
        <span className={statusClass}>{result.status.toUpperCase()}</span>
      </div>

      {result.explanation && (
        <div className="result-section">
          <h4>Explanation</h4>
          <p>{result.explanation}</p>
        </div>
      )}

      {Array.isArray(result.evidence) && result.evidence.length > 0 && (
        <div className="result-section">
          <h4>Evidence Found</h4>
          <ul>
            {result.evidence.map((ev, idx) => (
              <li key={idx}>{ev}</li>
            ))}
          </ul>
        </div>
      )}
    </div>
  );
}

export default ResultCard;