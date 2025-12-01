import React, { useRef } from "react";
import Hero from "./components/Hero";
import PredictionSection from "./components/PredictionSection";
import Footer from "./components/Footer";
import "./App.css";

const App = () => {
  const predictionRef = useRef(null);

  const scrollToPrediction = () => {
    predictionRef.current?.scrollIntoView({
      behavior: "smooth",
      block: "start",
    });
  };

  return (
    <section>
      <Hero onScroll={scrollToPrediction} />
      <div ref={predictionRef}>
        <PredictionSection />
      </div>
      <Footer />
    </section>
  );
};

export default App;
