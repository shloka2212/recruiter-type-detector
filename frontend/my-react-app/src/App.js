import React, { useState } from "react";
import "./App.css";
import JobForm from "./components/JobForm";
import ResultCard from "./components/ResultCard";

function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  // --- No changes to this function ---
  const onAnalyze = async (description) => {
    setLoading(true);
    setResult(null); // Clear previous results before new analysis
    try {
      // IMPORTANT: Replace with your actual backend URL when deployed
      const res = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ description }),
      });
      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error("Failed to connect to the backend:", err);
      setResult({
        // Provide a more descriptive error object
        status: "error",
        explanation: "Could not connect to the analysis server. Please make sure it's running and accessible.",
        evidence: [],
      });
    } finally {
      setLoading(false);
    }
  };

  // --- NEW: Function to clear the form and results ---
  const onClear = () => {
    setResult(null);
  };

  return (
    <div className="page">
      {/* --- NEW: Header element --- */}
      <header className="app-header">
        {/* You can add a logo or more complex navigation here later */}
      </header>

      {/* Main content area */}
      <main>
        <div className="container">
          {/* --- NEW: Title and Tagline --- */}
          <h1>Recruiter Type Detector</h1>
          <p className="tagline">
            Paste a job description to instantly identify its source.
          </p>

          {/* --- UPDATED: Pass the new onClear function --- */}
          <JobForm onAnalyze={onAnalyze} onClear={onClear} loading={loading} />
        </div>

        {/* --- Result card is now wrapped in the main element --- */}
        <ResultCard result={result} loading={loading} />
      </main>

      {/* --- NEW: Footer element --- */}
      <footer className="app-footer">
        <p>
          Made by{" "}
          <a
            href="https://github.com/shloka2212"
            target="_blank"
            rel="noopener noreferrer"
          >
            Shloka Bhatt
          </a>
        </p>
      </footer>
    </div>
  );
}

export default App;