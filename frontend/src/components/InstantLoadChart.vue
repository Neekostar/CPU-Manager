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
    };
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      try {
        const response = await axios.get('http://localhost:8000/cpu_load_last_hour');
        this.instantLoadData = response.data;
        this.drawChart();
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    },
    drawChart() {
      const ctx = document.getElementById('instant-load-chart').getContext('2d');
      new Chart(ctx, {
        type: 'line',
        data: {
          labels: this.instantLoadData.map(entry => entry.timestamp),
          datasets: [{
            label: 'Instant CPU Load',
            data: this.instantLoadData.map(entry => entry.value),
            borderColor: 'rgb(75, 192, 192)',
            fill: false,
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
                  minute: 'yyyy-MM-dd HH:mm:ss',
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
              }
            }
          }
        }
      });
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
