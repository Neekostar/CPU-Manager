import { createRouter, createWebHistory } from 'vue-router';
import Home from './components/Home.vue';
import InstantLoadChart from './components/InstantLoadChart.vue';
import AverageLoadChart from './components/AverageLoadChart.vue';

const routes = [
  { path: '/', component: Home },
  { path: '/instant-load', component: InstantLoadChart },
  { path: '/average-load', component: AverageLoadChart },
];

const router = createRouter({
  history: createWebHistory(),
  routes,
});

export default router;
