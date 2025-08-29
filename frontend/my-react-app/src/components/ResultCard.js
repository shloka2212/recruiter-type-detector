import React from "react";

function ResultCard({ result }) {
  if (!result) return null;

  if (result.error) {
    return (
      <div className="result-box fade-in" style={{ borderLeftColor: "#e74c3c" }}>
        <h3 style={{ color: "#e74c3c" }}>Error</h3>
        <p>{result.error}</p>
      </div>
    );
  }

  const statusClass = result.status === "real" ? "status real" : "status consulting";

  return (
    <div className="result-box fade-in">
      <h3>
        Status: <span className={statusClass}>{result.status.toUpperCase()}</span>
      </h3>

      {Array.isArray(result.evidence) && result.evidence.length > 0 && (
        <>
          <h4>Evidence:</h4>
          <ul>
            {result.evidence.map((ev, idx) => (
              <li key={idx}>{ev}</li>
            ))}
          </ul>
        </>
      )}

      {result.explanation && (
        <>
          <h4>Explanation:</h4>
          <p>{result.explanation}</p>
        </>
      )}
    </div>
  );
}

export default ResultCard;
