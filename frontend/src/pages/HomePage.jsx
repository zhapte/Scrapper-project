import { useState } from 'react'
import { getMe, getProducts, seedProducts } from '../api/testing.js'
import './HomePage.css'

function HomePage({ user, onLogout }) {
  const [apiResult, setApiResult] = useState(null)
  const [apiError, setApiError] = useState('')
  const [isLoading, setIsLoading] = useState(false)

  async function runApiCommand(command) {
    setApiError('')
    setApiResult(null)
    setIsLoading(true)

    try {
      const result = await command()
      setApiResult(result)
    } catch (error) {
      setApiError(error.message)
    } finally {
      setIsLoading(false)
    }
  }

  return (
    <main className="home-page">
      <header className="home-header">
        <div>
          <p>Scraper</p>
          <h1>Home</h1>
        </div>
        <button type="button" onClick={onLogout}>
          Logout
        </button>
      </header>

      <section className="home-content">
        <h2>Welcome, {user.first_name}</h2>
        <p>{user.email}</p>
      </section>

      <section className="api-test-panel" aria-labelledby="api-test-title">
        <h2 id="api-test-title">API Testing</h2>
        <div className="api-test-actions">
          <button
            type="button"
            onClick={() => runApiCommand(getMe)}
            disabled={isLoading}
          >
            Check Current User
          </button>
          <button
            type="button"
            onClick={() => runApiCommand(seedProducts)}
            disabled={isLoading}
          >
            Seed Products
          </button>
          <button
            type="button"
            onClick={() => runApiCommand(getProducts)}
            disabled={isLoading}
          >
            Get Products
          </button>
        </div>

        {isLoading && <p className="api-test-status">Running request...</p>}
        {apiError && <p className="api-test-error">{apiError}</p>}
        {apiResult && (
          <pre className="api-test-output">
            {JSON.stringify(apiResult, null, 2)}
          </pre>
        )}
      </section>
    </main>
  )
}

export default HomePage
