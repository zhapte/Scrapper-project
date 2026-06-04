import { useEffect, useState } from 'react'
import {
  clearStoredToken,
  getCurrentUser,
  getStoredToken,
  setStoredToken,
} from './api/auth.js'
import AuthPage from './pages/AuthPage.jsx'
import HomePage from './pages/HomePage.jsx'

function App() {
  const [currentUser, setCurrentUser] = useState(null)
  const [isCheckingSession, setIsCheckingSession] = useState(true)

  useEffect(() => {
    async function restoreSession() {
      const token = getStoredToken()

      if (!token) {
        setIsCheckingSession(false)
        return
      }

      try {
        const user = await getCurrentUser(token)
        setCurrentUser(user)
      } catch {
        clearStoredToken()
      } finally {
        setIsCheckingSession(false)
      }
    }

    restoreSession()
  }, [])

  function handleAuthenticated(authData) {
    setStoredToken(authData.access_token)
    setCurrentUser(authData.user)
  }

  function handleLogout() {
    clearStoredToken()
    setCurrentUser(null)
  }

  if (isCheckingSession) {
    return (
      <main className="auth-page">
        <p>Loading...</p>
      </main>
    )
  }

  if (currentUser) {
    return (
      <HomePage
        user={currentUser}
        onLogout={handleLogout}
      />
    )
  }

  return <AuthPage onAuthenticated={handleAuthenticated} />
}

export default App
