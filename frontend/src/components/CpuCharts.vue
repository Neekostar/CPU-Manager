<template>
  <div>
    <h1>CPU Load Monitoring</h1>
    <div class="chart-container">
      <canvas id="instant-load-chart"></canvas>
    </div>
    <div class="chart-container">
      <canvas id="average-load-chart"></canvas>
    </div>
  </div>
</template>

<script>
import axios from 'axios';
import {Chart, registerables} from 'chart.js';
import 'chartjs-adapter-date-fns';

// Register all necessary components for Chart.js
Chart.register(...registerables);

export default {
  data() {
    return {
      instantLoadData: [],
      averageLoadData: [],
    };
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      try {
        const instantLoadResponse = await axios.get('http://localhost:8000/cpu_load_last_hour');
        const averageLoadResponse = await axios.get('http://localhost:8000/average_load_last_hour');

        this.instantLoadData = instantLoadResponse.data;
        this.averageLoadData = averageLoadResponse.data;

        this.drawCharts();
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    },
    drawCharts() {
      const instantLoadCtx = document.getElementById('instant-load-chart').getContext('2d');
      new Chart(instantLoadCtx, {
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

      const averageLoadCtx = document.getElementById('average-load-chart').getContext('2d');
      new Chart(averageLoadCtx, {
        type: 'line',
        data: {
          labels: this.averageLoadData.map(entry => entry.timestamp),
          datasets: [{
            label: 'Average CPU Load',
            data: this.averageLoadData.map(entry => entry.average_load),
            borderColor: 'rgb(255, 99, 132)',
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
                tooltipFormat: 'yyyy-MM-dd HH:mm',
                displayFormats: {
                  minute: 'yyyy-MM-dd HH:mm',
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
                text: 'Average CPU Load (%)'
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
  height: 400px; /* Increase the height for better visibility */
  margin: 20px auto;
}

canvas {
  display: block;
  width: 100% !important;
  height: 100% !important;
}
</style>
