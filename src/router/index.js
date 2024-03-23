import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    redirect: { name: 'Sankey Diagram' },
  },
  {
    path: '/basic_data',
    name: 'Basic Data',
    component: () => import('@/views/basic_data.vue'),
  },
  {
    path: '/sankey_diagram',
    name: 'Sankey Diagram',
    component: () => import('@/views/sankey_diagram.vue'),
  },
  {
    path: '/position_diagram',
    name: 'Position Diagram',
    component: () => import('@/views/position_diagram/index.vue'),
  },
]

const router = createRouter({
  history: createWebHistory(),
  routes,
})

export default router
