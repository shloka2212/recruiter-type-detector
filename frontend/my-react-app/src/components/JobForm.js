import React, { useState } from "react";

function JobForm({ onAnalyze, loading }) {
  const [description, setDescription] = useState("");

  const handleSubmit = (e) => {
    e.preventDefault();
    if (description.trim()) onAnalyze(description);
  };

  const handleClear = () => {
    setDescription("");
  };

  return (
    <form onSubmit={handleSubmit}>
      <textarea
        placeholder="Paste the job description here..."
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        rows={6}
        cols={60}
      />
      <br />
      <div className="center-container" style={{ gap: 10 }}>
        <button type="submit" disabled={loading}>
          {loading ? (
            <span className="loading-dots">
              Analyzing<span>.</span><span>.</span><span>.</span>
            </span>
          ) : (
            "Analyze"
          )}
        </button>
        <button type="button" onClick={handleClear} disabled={loading}>
          Clear
        </button>
      </div>
    </form>
  );
}

export default JobForm;
