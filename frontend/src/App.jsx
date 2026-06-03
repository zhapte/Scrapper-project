import { useState } from 'react'
import AuthPage from './pages/AuthPage.jsx'
import HomePage from './pages/HomePage.jsx'

function App() {
  const [currentUser, setCurrentUser] = useState(null)

  if (currentUser) {
    return (
      <HomePage
        user={currentUser}
        onLogout={() => setCurrentUser(null)}
      />
    )
  }

  return <AuthPage onAuthenticated={setCurrentUser} />
}

export default App
