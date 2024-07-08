<template>
  <div class="app-container bg-dark text-light min-vh-100">
    <div class="text-center py-4">
      <h1>CPU Load Monitoring</h1>
      <nav class="my-4">
        <router-link to="/">
          <button class="btn btn-primary mx-2">Home</button>
        </router-link>
        <router-link to="/instant-load">
          <button class="btn btn-primary mx-2">Instant Load Chart</button>
        </router-link>
        <router-link to="/average-load">
          <button class="btn btn-primary mx-2">Average Load Chart</button>
        </router-link>
      </nav>
    </div>
    <router-view></router-view>
  </div>
</template>

<script>
export default {
  name: 'App',
}
</script>

<style scoped>
.app-container {
  background-color: #242424;
  font-family: 'Inter', system-ui, Avenir, Helvetica, Arial, sans-serif;
  line-height: 1.5;
  font-weight: 400;
}
</style>
