<template>
  <div id="app">
    <header>
      <h1>FinAssistant</h1>
      <nav>
        <router-link to="/">Portfolio</router-link>
        <router-link to="/import">Import</router-link>
        <router-link to="/analysis">Analysis</router-link>
        <router-link to="/news">News</router-link>
      </nav>
    </header>
    <main>
      <router-view></router-view>
    </main>
    <footer>
      <p>Backend Status: {{ backendStatus }}</p>
    </footer>
  </div>
</template>

<script>
export default {
  name: 'App',
  data() {
    return {
      backendStatus: 'Connecting...'
    }
  },
  mounted() {
    this.checkBackend()
  },
  methods: {
    async checkBackend() {
      try {
        const response = await fetch('/api/health')
        const data = await response.json()
        this.backendStatus = data.status || 'unknown'
      } catch (e) {
        this.backendStatus = 'Offline'
      }
    }
  }
}
</script>

<style scoped>
</style>
