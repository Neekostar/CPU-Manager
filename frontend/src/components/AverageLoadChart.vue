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
      const chartData = this.processData(this.averageLoadData);

      new Chart(ctx, {
        type: 'line',
        data: {
          datasets: [{
            label: 'Average CPU Load',
            data: chartData,
            borderColor: 'rgb(255, 99, 132)',
            fill: false,
            spanGaps: false,
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
    },
    processData(data) {
      const processedData = [];
      for (let i = 0; i < data.length; i++) {
        const currentEntry = data[i];
        const nextEntry = data[i + 1];

        // Check if nextEntry exists and if the difference is less than a minute
        if (nextEntry && Math.abs(new Date(nextEntry.timestamp) - new Date(currentEntry.timestamp)) > 60000) {
          processedData.push({ x: new Date(currentEntry.timestamp), y: null });
        } else {
          processedData.push({ x: new Date(currentEntry.timestamp), y: currentEntry.average_load });
        }
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
