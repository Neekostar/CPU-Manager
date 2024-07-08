<template>
  <div class="container text-center text-light mt-5">
    <div class="card bg-dark text-light">
      <div class="card-body">
        <h1 class="mb-4">Welcome to CPU Load Monitoring</h1>
        <p class="lead">
          Monitor and analyze the CPU load in real-time and average metrics. Navigate through the application to view instant and average CPU load charts.
        </p>
      </div>
    </div>
  </div>
</template>

<script>
export default {
  name: 'Home',
}
</script>

<style scoped>
.container {
  max-width: 800px;
}

.card {
  border: none;
  border-radius: 10px;
  padding: 20px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}
</style>
