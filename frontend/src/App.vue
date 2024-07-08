<!-- src/App.vue -->
<template>
  <div id="app">
    <CpuCharts />
  </div>
</template>

<script>
import CpuCharts from './components/CpuCharts.vue';

export default {
  name: 'App',
  components: {
    CpuCharts
  }
}
</script>
