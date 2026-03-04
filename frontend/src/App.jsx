import { useState, useEffect } from 'react'

function App() {
  const [status, setStatus] = useState(null)

  useEffect(() => {
    fetch('/api/health')
      .then(res => res.json())
      .then(data => setStatus(data))
      .catch(err => console.error(err))
  }, [])

  return (
    <div className="app">
      <header>
        <h1>FinAssistant</h1>
        <nav>
          <a href="#portfolio">Portfolio</a>
          <a href="#news">News</a>
          <a href="#analysis">Analysis</a>
        </nav>
      </header>
      <main>
        <section id="portfolio">
          <h2>Portfolio</h2>
          <p>Track and manage your investments</p>
        </section>
        <section id="news">
          <h2>News</h2>
          <p>Latest financial news and market updates</p>
        </section>
        <section id="analysis">
          <h2>Analysis</h2>
          <p>Market analysis and sentiment tracking</p>
        </section>
      </main>
      <footer>
        <p>Backend Status: {status ? status.status : 'Connecting...'}</p>
      </footer>
    </div>
  )
}

export default App
