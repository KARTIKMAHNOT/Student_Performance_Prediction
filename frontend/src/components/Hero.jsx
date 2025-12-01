
import heroImg from "../assets/hero.png";
import "./hero.css";

function Hero({ onScroll }) {


  return (
    <section className="hero">
      <div className="hero-background"></div>


        <div className="hero-left">
          <div className="title-container">
            <h1 className="title">IntelliMarks</h1>
            <div className="title-underline"></div>
          </div>

          <p className="tag">Predict • Analyse • Improve</p>
          <p className="desc">
            Advanced AI-powered student performance prediction system that helps
            educators identify at-risk students and optimize learning outcomes
            through data-driven insights.
          </p>

          <div className="feature-list">
            <div className="feature">
              <span className="feature-icon">🎯</span>
              <span>Accurate Predictions</span>
            </div>
            <div className="feature">
              <span className="feature-icon">📊</span>
              <span>Detailed Analytics</span>
            </div>
            <div className="feature">
              <span className="feature-icon">🚀</span>
              <span>Actionable Insights</span>
            </div>
          </div>

          <button className="start-btn" onClick={onScroll}>
            <span className="btn-text">Start Prediction</span>
            <span className="btn-arrow">↓</span>
            <div className="btn-shine"></div>
          </button>
        </div>

        <div className="hero-right">
          <div className="image-container">
            <img
              src={heroImg}
              alt="AI Education Analytics Illustration"
              className="hero-img"
            />
            <div className="image-glow"></div>
          </div>
        </div>
    </section>
  );
}

export default Hero;
