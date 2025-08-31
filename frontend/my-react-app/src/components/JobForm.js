import React, { useState } from "react";

// Icon component for the "Analyze" button
const SearchIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" width="20" height="20" >
    <path strokeLinecap="round" strokeLinejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" />
  </svg>
);

// Icon component for the "Clear" button
const ClearIcon = () => (
  <svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor" width="20" height="20" >
    <path strokeLinecap="round" strokeLinejoin="round" d="M9.75 9.75l4.5 4.5m0-4.5l-4.5 4.5M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
  </svg>
);


function JobForm({ onAnalyze, onClear, loading }) {
  const [description, setDescription] = useState("");

  // This function calls the onAnalyze prop passed from App.js
  const handleSubmit = (e) => {
    e.preventDefault();
    if (description.trim()) {
      onAnalyze(description);
    }
  };

  // This function clears the textarea AND the result card in App.js
  const handleClear = () => {
    setDescription("");
    onClear(); // This is the new, important part
  };

  return (
    <form onSubmit={handleSubmit}>
      <textarea
        placeholder="Paste the full job description here to see the magic happen..."
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        disabled={loading}
      />

      {/* --- UPDATED: New container and button classes --- */}
      <div className="button-container">
        <button
          type="submit"
          className="button button-primary"
          disabled={loading || !description.trim()}
        >
          <SearchIcon />
          <span>{loading ? "Analyzing..." : "Analyze"}</span>
        </button>

        <button
          type="button"
          className="button button-secondary"
          onClick={handleClear}
          disabled={loading}
        >
          <ClearIcon />
          <span>Clear</span>
        </button>
      </div>
    </form>
  );
}

export default JobForm;