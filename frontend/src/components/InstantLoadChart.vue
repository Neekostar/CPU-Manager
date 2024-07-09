<template>
  <div class="chart-container">
    <canvas id="instant-load-chart"></canvas>
  </div>
</template>

<script>
import axios from 'axios';
import { Chart, registerables } from 'chart.js';
import 'chartjs-adapter-date-fns';

Chart.register(...registerables);

export default {
  data() {
    return {
      instantLoadData: [],
      gaps: []
    };
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      try {
        const response = await axios.get('http://localhost:8000/cpu_loads_with_gaps');
        this.instantLoadData = response.data.cpu_loads;
        this.gaps = response.data.gaps;
        this.drawChart();
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    },
    drawChart() {
      const ctx = document.getElementById('instant-load-chart').getContext('2d');
      const chartData = this.processData(this.instantLoadData);

      new Chart(ctx, {
        type: 'line',
        data: {
          datasets: [{
            label: 'Instant CPU Load',
            data: chartData,
            borderColor: 'rgb(75, 192, 192)',
            backgroundColor: 'rgba(75, 192, 192, 0.4)',
            fill: false,
            spanGaps: false
          }]
        },
        options: {
          responsive: true,
          maintainAspectRatio: false,
          scales: {
            x: {
              type: 'time',
              time: {
                unit: 'minute',
                tooltipFormat: 'yyyy-MM-dd HH:mm:ss',
                displayFormats: {
                  minute: 'yyyy-MM-dd HH:mm:ss'
                }
              },
              title: {
                display: true,
                text: 'Time'
              }
            },
            y: {
              title: {
                display: true,
                text: 'CPU Load (%)'
              },
              beginAtZero: true
            }
          }
        }
      });
    },
    processData(data) {
      const processedData = [];
      const threshold = 10000; // 10 секунд в миллисекундах

      for (let i = 0; i < data.length; i++) {
        const current = data[i];
        const currentTime = new Date(current.timestamp);

        if (i > 0) {
          const previous = data[i - 1];
          const previousTime = new Date(previous.timestamp);

          // Если разница между текущей и предыдущей записью больше 10 секунд, добавляем null
          if (currentTime - previousTime > threshold) {
            processedData.push({ x: previousTime, y: null });
            processedData.push({ x: currentTime, y: null });
          }
        }

        processedData.push({ x: currentTime, y: current.value });
      }

      return processedData;
    }
  }
}
</script>

<style scoped>
.chart-container {
  position: relative;
  width: 100%;
  height: 400px;
  margin: 20px auto;
  background-color: #343a40; /* Dark background */
  padding: 20px;
  border-radius: 8px;
}

canvas {
  display: block;
  width: 100% !important;
  height: 100% !important;
}
</style>
