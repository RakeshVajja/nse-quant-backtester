import React, { useEffect, useRef, useState } from "react";
import axios from "axios";
import { createChart, CandlestickSeries } from "lightweight-charts";

function App() {
  const chartContainerRef = useRef(null);
  const [symbol, setSymbol] = useState("RELIANCE.NS");

  const renderChart = (data, patterns) => {
    if (!chartContainerRef.current) return;

    chartContainerRef.current.innerHTML = "";

    const chart = createChart(chartContainerRef.current, {
      width: 1000,
      height: 500,
    });

    const candleSeries = chart.addSeries(CandlestickSeries);

    const formattedData = data.map((item) => ({
      time: Math.floor(new Date(item.datetime).getTime() / 1000),
      open: item.open,
      high: item.high,
      low: item.low,
      close: item.close,
    }));

    candleSeries.setData(formattedData);

    const markers = patterns
      .filter((p) => formattedData[p.index])
      .map((p) => ({
        time: formattedData[p.index].time,
        position:
          p.pattern === "Bullish Engulfing" || p.pattern === "Hammer"
            ? "belowBar"
            : "aboveBar",
        color: getPatternColor(p.pattern),
        shape:
          p.pattern === "Bullish Engulfing" || p.pattern === "Hammer"
            ? "arrowUp"
            : "arrowDown",
        text: p.pattern,
      }));

    candleSeries.setMarkers(markers);
  };

  const fetchData = async (stock) => {
    const response = await axios.get(
      `http://127.0.0.1:8000/stock/${stock}`
    );

    const data = response.data.data;
    const patterns = response.data.patterns;

    renderChart(data, patterns);
  };

  useEffect(() => {
    fetchData(symbol);
  }, []); // load once on mount

  const getPatternColor = (pattern) => {
    switch (pattern) {
      case "Bullish Engulfing":
        return "green";
      case "Bearish Engulfing":
        return "red";
      case "Hammer":
        return "blue";
      case "Shooting Star":
        return "orange";
      case "Doji":
        return "purple";
      default:
        return "gray";
    }
  };

  return (
    <div style={{ padding: "20px" }}>
      <h2>NSE Candlestick Pattern Visualizer</h2>

      <input
        value={symbol}
        onChange={(e) => setSymbol(e.target.value)}
      />

      <button onClick={() => fetchData(symbol)}>
        Load
      </button>

      <div ref={chartContainerRef} />
    </div>
  );
}

export default App;