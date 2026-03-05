import Vue from 'vue'
import VueRouter from 'vue-router'
import Portfolio from '@/views/Portfolio.vue'
import News from '@/views/News.vue'
import Analysis from '@/views/Analysis.vue'
import Import from '@/views/Import.vue'

Vue.use(VueRouter)

const routes = [
  {
    path: '/',
    name: 'Portfolio',
    component: Portfolio
  },
  {
    path: '/news',
    name: 'News',
    component: News
  },
  {
    path: '/analysis',
    name: 'Analysis',
    component: Analysis
  },
  {
    path: '/import',
    name: 'Import',
    component: Import
  }
]

const router = new VueRouter({
  mode: 'history',
  base: process.env.BASE_URL,
  routes
})

export default router
