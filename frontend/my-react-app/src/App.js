import React, { useState } from "react";
import "./App.css";
import JobForm from "./components/JobForm";
import ResultCard from "./components/ResultCard";

function App() {
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  const onAnalyze = async (description) => {
    setLoading(true);
    setResult(null);
    try {
      const res = await fetch("http://127.0.0.1:8000/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ description }),
      });
      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error(err);
      setResult({ error: "Error connecting to backend" });
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="page">
      <div className="container">
        <h1>Recruiter Type Detector</h1>
        <JobForm onAnalyze={onAnalyze} loading={loading} />
      </div>

      <ResultCard result={result} />
    </div>
  );
}

export default App;
