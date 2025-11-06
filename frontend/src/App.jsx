import React, { useState, useEffect } from "react";
import { Line } from "react-chartjs-2";
import {
  Chart as ChartJS,
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend,
} from "chart.js";

// Регистрируем элементы графика
ChartJS.register(
  CategoryScale,
  LinearScale,
  PointElement,
  LineElement,
  Title,
  Tooltip,
  Legend
);

function App() {
  const [dataPoints, setDataPoints] = useState([]);

  // Добавляем случайные данные каждую секунду
  useEffect(() => {
    const interval = setInterval(() => {
      setDataPoints(prev => [...prev.slice(-9), Math.floor(Math.random() * 100)]);
    }, 1000);

    return () => clearInterval(interval);
  }, []);

  const data = {
    labels: dataPoints.map((_, i) => i + 1),
    datasets: [
      {
        label: "Случайные данные",
        data: dataPoints,
        borderColor: "rgb(75, 192, 192)",
        backgroundColor: "rgba(75, 192, 192, 0.2)",
      },
    ],
  };

  const options = {
    responsive: true,
    plugins: {
      legend: { position: "top" },
      title: { display: true, text: "Простая визуализация на React + Chart.js" },
    },
  };

  return (
    <div style={{ width: "600px", margin: "50px auto" }}>
      <Line data={data} options={options} />
    </div>
  );
}

export default App;
