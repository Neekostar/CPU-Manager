<template>
  <div class="chart-container">
    <canvas id="average-load-chart"></canvas>
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
      averageLoadData: [],
    };
  },
  mounted() {
    this.fetchData();
  },
  methods: {
    async fetchData() {
      try {
        const response = await axios.get('http://localhost:8000/average_load_last_hour');
        this.averageLoadData = response.data;
        this.drawChart();
      } catch (error) {
        console.error('Error fetching data:', error);
      }
    },
    drawChart() {
      const ctx = document.getElementById('average-load-chart').getContext('2d');
      new Chart(ctx, {
        type: 'line',
        data: {
          labels: this.averageLoadData.map(entry => entry.timestamp),
          datasets: [{
            label: 'Average CPU Load',
            data: this.averageLoadData.map(entry => entry.average_load),
            borderColor: 'rgb(255, 99, 132)',
            fill: false,
            spanGaps: true,
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
