import { useState } from "react";
import axios from "axios";
import "./prediction.css";
import Suggestions from "./Suggestions";

export default function PredictionSection() {
  const [form, setForm] = useState({
    Gender: 1,
    Study_Hours_per_Week: 10,
    Attendance_Rate: 85,
    Past_Exam_Scores: 75,
    Internet_Access_at_Home: 1,
    Extracurricular_Activities: 0,
    Parent_Edu_Bachelors: 0,
    Parent_Edu_High_School: 0,
    Parent_Edu_Masters: 0,
    Parent_Edu_PhD: 1,
  });

  const [score, setScore] = useState(null);
  const [status, setStatus] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState(null);
  const [showResults, setShowResults] = useState(false);
  const [Suggest, setSuggest] = useState(false);
  const numberChange = (e) =>
    setForm({ ...form, [e.target.name]: Number(e.target.value) });

  const setEdu = (key) => {
    setForm({
      ...form,
      Parent_Edu_High_School: 0,
      Parent_Edu_Bachelors: 0,
      Parent_Edu_Masters: 0,
      Parent_Edu_PhD: 0,
      [key]: 1,
    });
  };

  const predict = async () => {
    setLoading(true);
    setError(null);
    setShowResults(false);
    setSuggest(false);

    try {
      const [s, p] = await Promise.all([
        axios.post("http://127.0.0.1:8001/predict-score", form),
        axios.post("http://127.0.0.1:8001/predict-passfail", form),
      ]);

      setScore(s.data.predicted_score);
      setStatus(p.data);
      setShowResults(true);

      setTimeout(() => {
        document.querySelector(".results-container")?.scrollIntoView({
          behavior: "smooth",
          block: "center",
        });
      }, 300);
    } catch (err) {
      setError("Prediction Error — Please check backend server ❗");
    }

    setLoading(false);
  };

  const resetForm = () => {
    setForm({
      Gender: 1,
      Study_Hours_per_Week: 10,
      Attendance_Rate: 85,
      Past_Exam_Scores: 75,
      Internet_Access_at_Home: 1,
      Extracurricular_Activities: 0,
      Parent_Edu_Bachelors: 0,
      Parent_Edu_High_School: 0,
      Parent_Edu_Masters: 0,
      Parent_Edu_PhD: 1,
    });
    setScore(null);
    setStatus(null);
    setShowResults(false);
    setSuggest(false);
    setError(null);
  };

  const edu = form.Parent_Edu_High_School
    ? "High School"
    : form.Parent_Edu_Bachelors
    ? "Bachelors"
    : form.Parent_Edu_Masters
    ? "Masters"
    : form.Parent_Edu_PhD
    ? "PhD"
    : "None";

  const getScoreColor = (score) => {
    if (score >= 80) return "var(--success)";
    if (score >= 60) return "var(--accent-2)";
    return "var(--danger)";
  };

  const getStatusIcon = (status) => {
    return status?.result === "Pass" ? "✅" : "❌";
  };

  return (
    <section className="predict-section" id="prediction">
      <div className="section-header">
        <h2>Student Performance Prediction</h2>
        <p>Enter student details to predict academic performance</p>
      </div>

      <div className="prediction-container">
        <div className="form-container glass">
          <div className="form-header">
            <h3>Student Information</h3>
          </div>

          <div className="form-grid">
            <div className="input-group">
              <label className="input-label">Gender</label>
              <select
                name="Gender"
                value={form.Gender}
                onChange={numberChange}
                className="form-input"
              >
                <option value={1}>Male</option>
                <option value={0}>Female</option>
              </select>
            </div>
            <div className="input-group">
              <label className="input-label">
                Study Hours / Week
                <span className="value-display">
                  {form.Study_Hours_per_Week}h
                </span>
              </label>
              <input
                type="range"
                name="Study_Hours_per_Week"
                min="0"
                max="40"
                value={form.Study_Hours_per_Week}
                onChange={numberChange}
                className="form-slider"
              />
              <div className="slider-labels">
                <span>0h</span>
                <span>40h</span>
              </div>
            </div>
            <div className="input-group">
              <label className="input-label">
                Attendance Rate
                <span className="value-display">{form.Attendance_Rate}%</span>
              </label>
              <input
                type="range"
                name="Attendance_Rate"
                min="0"
                max="100"
                value={form.Attendance_Rate}
                onChange={numberChange}
                className="form-slider"
              />
              <div className="slider-labels">
                <span>0%</span>
                <span>100%</span>
              </div>
            </div>
            <div className="input-group">
              <label className="input-label">
                Past Exam Scores
                <span className="value-display">{form.Past_Exam_Scores}%</span>
              </label>
              <input
                type="range"
                name="Past_Exam_Scores"
                min="0"
                max="100"
                value={form.Past_Exam_Scores}
                onChange={numberChange}
                className="form-slider"
              />
              <div className="slider-labels">
                <span>0%</span>
                <span>100%</span>
              </div>
            </div>
            <div className="input-group">
              <label className="input-label">Internet Access at Home</label>
              <div className="toggle-group">
                <button
                  type="button"
                  className={`toggle-btn ${
                    form.Internet_Access_at_Home ? "active" : ""
                  }`}
                  onClick={() =>
                    setForm({ ...form, Internet_Access_at_Home: 1 })
                  }
                >
                  Yes
                </button>
                <button
                  type="button"
                  className={`toggle-btn ${
                    !form.Internet_Access_at_Home ? "active" : ""
                  }`}
                  onClick={() =>
                    setForm({ ...form, Internet_Access_at_Home: 0 })
                  }
                >
                  No
                </button>
              </div>
            </div>
            <div className="input-group">
              <label className="input-label">Extracurricular Activities</label>
              <div className="toggle-group">
                <button
                  type="button"
                  className={`toggle-btn ${
                    form.Extracurricular_Activities ? "active" : ""
                  }`}
                  onClick={() =>
                    setForm({ ...form, Extracurricular_Activities: 1 })
                  }
                >
                  Yes
                </button>
                <button
                  type="button"
                  className={`toggle-btn ${
                    !form.Extracurricular_Activities ? "active" : ""
                  }`}
                  onClick={() =>
                    setForm({ ...form, Extracurricular_Activities: 0 })
                  }
                >
                  No
                </button>
              </div>
            </div>
            <div className="input-group full-width">
              <label className="input-label">Parent Education Level</label>
              <div className="edu-grid">
                <button
                  onClick={() => setEdu("Parent_Edu_High_School")}
                  className={`edu-btn ${
                    form.Parent_Edu_High_School ? "active" : ""
                  }`}
                >
                  🏫 High School
                </button>
                <button
                  onClick={() => setEdu("Parent_Edu_Bachelors")}
                  className={`edu-btn ${
                    form.Parent_Edu_Bachelors ? "active" : ""
                  }`}
                >
                  🎓 Bachelors
                </button>
                <button
                  onClick={() => setEdu("Parent_Edu_Masters")}
                  className={`edu-btn ${
                    form.Parent_Edu_Masters ? "active" : ""
                  }`}
                >
                  📚 Masters
                </button>
                <button
                  onClick={() => setEdu("Parent_Edu_PhD")}
                  className={`edu-btn ${form.Parent_Edu_PhD ? "active" : ""}`}
                >
                  🔬 PhD
                </button>
              </div>
              <div className="selected-edu">
                Currently Selected: <strong>{edu}</strong>
              </div>
            </div>
          </div>
          <div className="form-actions">
            <button className="reset-btn" onClick={resetForm}>
              Reset Form
            </button>
            <button
              className="predict-btn"
              onClick={predict}
              disabled={loading}
            >
              {loading ? (
                <>
                  {" "}
                  <div className="spinner"></div> Predicting...{" "}
                </>
              ) : (
                "🔮 Predict Results"
              )}
            </button>
          </div>
          {showResults && (
            <div className="suggestion-wrapper">
              {!Suggest ? (
                <button
                  className="suggestion-btn"
                  onClick={() => setSuggest(true)}
                >
                  🤖 Generate AI Suggestions
                </button>
              ) : (
                <Suggestions
                  study={form.Study_Hours_per_Week}
                  attendance={form.Attendance_Rate}
                  past_score={form.Past_Exam_Scores}
                  predicted_score={score}
                />
              )}
            </div>
          )}

          {error && <p className="error-message">⚠ {error}</p>}
        </div>
        {showResults && (
          <div className="results-container glass">
            <div className="results-header">
              <h3>Prediction Results</h3>
              <div className="results-badge">{getStatusIcon(status)}</div>
            </div>

            <div className="results-content">
              <div className="score-display">
                <div className="score-ring">
                  <div
                    className="score-progress"
                    style={{
                      background: `conic-gradient(${getScoreColor(score)} ${
                        (score / 100) * 360
                      }deg, var(--glass) 0deg)`,
                    }}
                  ></div>
                  <div className="score-value">
                    <span>{score?.toFixed(1)}</span>
                    <small>/100</small>
                  </div>
                </div>
                <div className="score-label">Predicted Score</div>
              </div>
              <div className="status-display">
                <div className={`status-card ${status.result.toLowerCase()}`}>
                  <span className="status-icon">{getStatusIcon(status)}</span>
                  <span className="status-text">{status.result}</span>
                  <div className="confidence">
                    Confidence: <strong>{status.confidence}</strong>
                  </div>
                </div>
                <div className="insights">
                  <h4>Key Insights</h4>
                  <ul>
                    <li>📊 Based on comprehensive analysis of input values</li>
                    <li>
                      {score >= 60
                        ? "🎯 Strong chance of success"
                        : "⚠ Needs improvement to achieve success"}
                    </li>
                    <li>
                      {form.Study_Hours_per_Week < 15
                        ? "💡 Try increasing weekly study time"
                        : "📘 Study hours look stable"}
                    </li>
                  </ul>
                </div>
              </div>
            </div>
          </div>
        )}
      </div>
    </section>
  );
}
