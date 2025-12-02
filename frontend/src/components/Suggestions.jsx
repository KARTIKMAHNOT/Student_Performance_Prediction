import { useEffect, useState } from "react";
import "./suggestions.css";

export default function Suggestions({
  study,
  attendance,
  past_score,
  predicted_score,
}) {
  const [suggestions, setSuggestions] = useState(null);
  const [show, setShow] = useState(false);

  useEffect(() => {
    fetch("https://student-performance-prediction-wcqw.onrender.com/suggestion", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({
        study_hours: study,
        attendance,
        past_score,
        predicted_score,
      }),
    })
      .then((res) => res.json())
      .then((data) => {
        setSuggestions(data.suggestions);
        setTimeout(() => setShow(true), 200); 
      });
  }, []);

  return (
    <div className={`suggestion-card ${show && "show"}`}>
      <h2>🤖 AI-Generated Suggestions</h2>

      {!suggestions ? (
        <div className="loader">Thinking...</div>
      ) : (
        <ul>
          {suggestions.map((s, i) => (
            <li key={i}>{s}</li>
          ))}
        </ul>
      )}
    </div>
  );
}
