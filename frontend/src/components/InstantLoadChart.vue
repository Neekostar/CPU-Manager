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

      // Преобразуем данные в активные сегменты и неактивные периоды
      const activeSegments = [];
      let currentSegment = [];

      this.instantLoadData.forEach(entry => {
        if (this.isActivePeriod(entry.timestamp)) {
          currentSegment.push({ x: entry.timestamp, y: entry.value });
        } else {
          if (currentSegment.length > 0) {
            activeSegments.push(currentSegment);
            currentSegment = [];
          }
          if (entry.value === null) {
            return;
          }
          currentSegment.push({x: entry.timestamp, y: 0});
        }
      });

      // Добавляем последний сегмент, если он не пустой
      if (currentSegment.length > 0) {
        activeSegments.push(currentSegment);
      }

      const inactiveSegments = this.gaps.filter(gap => !gap.is_active).map(gap => {
        return [
          { x: new Date(gap.start_time), y: 0 },
          { x: new Date(gap.end_time), y: 0 }
        ];
      });

      // Объединяем активные и неактивные сегменты
      const combinedSegments = [];
      let currentCombinedSegment = [];

      for (let i = 0; i < activeSegments.length; i++) {
        currentCombinedSegment = currentCombinedSegment.concat(activeSegments[i]);
        if (i < inactiveSegments.length) {
          currentCombinedSegment.push(inactiveSegments[i][0]);
          currentCombinedSegment = currentCombinedSegment.concat(inactiveSegments[i].slice(1));
        }
        if (i < activeSegments.length - 1) {
          currentCombinedSegment.push({
            x: activeSegments[i + 1][0].x,
            y: null,
            borderColor: 'rgb(75, 192, 192)'
          });
        }
      }

      combinedSegments.push(currentCombinedSegment);

      new Chart(ctx, {
        type: 'line',
        data: {
          datasets: [
            {
              label: 'CPU Load',
              data: combinedSegments.flat(),
              borderColor: 'rgb(75, 192, 192)',
              fill: false,
              spanGaps: true
            }
          ]
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
              }
            }
          }
        }
      });
    },
    isActivePeriod(timestamp) {
      // Проверяем, является ли данный момент времени активным периодом
      for (const gap of this.gaps) {
        if (!gap.is_active && timestamp >= gap.start_time && timestamp <= gap.end_time) {
          return false;
        }
      }
      return true;
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
