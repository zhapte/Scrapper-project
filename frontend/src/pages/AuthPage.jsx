import { useState } from 'react'
import { loginUser, registerUser } from '../api/auth.js'
import './AuthPage.css'

const initialLoginForm = {
  email: '',
  password: '',
}

const initialRegistrationForm = {
  firstName: '',
  lastName: '',
  email: '',
  password: '',
}

function AuthPage({ onAuthenticated }) {
  const [mode, setMode] = useState('login')
  const [loginForm, setLoginForm] = useState(initialLoginForm)
  const [registrationForm, setRegistrationForm] = useState(
    initialRegistrationForm,
  )
  const [errorMessage, setErrorMessage] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  const isLogin = mode === 'login'

  function handleLoginChange(event) {
    const { name, value } = event.target
    setLoginForm((currentForm) => ({
      ...currentForm,
      [name]: value,
    }))
  }

  function handleRegistrationChange(event) {
    const { name, value } = event.target
    setRegistrationForm((currentForm) => ({
      ...currentForm,
      [name]: value,
    }))
  }

  async function handleSubmit(event) {
    event.preventDefault()
    setErrorMessage('')
    setIsSubmitting(true)

    try {
      const authData = isLogin
        ? await loginUser(loginForm)
        : await registerUser({
            first_name: registrationForm.firstName,
            last_name: registrationForm.lastName,
            email: registrationForm.email,
            password: registrationForm.password,
          })

      onAuthenticated(authData)
    } catch (error) {
      setErrorMessage(error.message)
    } finally {
      setIsSubmitting(false)
    }
  }

  return (
    <main className="auth-page">
      <section className="auth-panel" aria-labelledby="auth-title">
        <div className="auth-header">
          <p className="auth-kicker">Scraper</p>
          <h1 id="auth-title">{isLogin ? 'Login' : 'Register'}</h1>
        </div>

        <div className="auth-tabs" aria-label="Authentication options">
          <button
            type="button"
            className={isLogin ? 'active' : ''}
            onClick={() => setMode('login')}
          >
            Login
          </button>
          <button
            type="button"
            className={!isLogin ? 'active' : ''}
            onClick={() => setMode('register')}
          >
            Register
          </button>
        </div>

        {errorMessage && <p className="auth-error">{errorMessage}</p>}

        {isLogin ? (
          <form className="auth-form" onSubmit={handleSubmit}>
            <label>
              Email
              <input
                name="email"
                type="email"
                value={loginForm.email}
                onChange={handleLoginChange}
                autoComplete="email"
                required
              />
            </label>

            <label>
              Password
              <input
                name="password"
                type="password"
                value={loginForm.password}
                onChange={handleLoginChange}
                autoComplete="current-password"
                required
              />
            </label>

            <button type="submit" disabled={isSubmitting}>
              {isSubmitting ? 'Logging in...' : 'Login'}
            </button>
          </form>
        ) : (
          <form className="auth-form" onSubmit={handleSubmit}>
            <label>
              First name
              <input
                name="firstName"
                type="text"
                value={registrationForm.firstName}
                onChange={handleRegistrationChange}
                autoComplete="given-name"
                required
              />
            </label>

            <label>
              Last name
              <input
                name="lastName"
                type="text"
                value={registrationForm.lastName}
                onChange={handleRegistrationChange}
                autoComplete="family-name"
                required
              />
            </label>

            <label>
              Email
              <input
                name="email"
                type="email"
                value={registrationForm.email}
                onChange={handleRegistrationChange}
                autoComplete="email"
                required
              />
            </label>

            <label>
              Password
              <input
                name="password"
                type="password"
                value={registrationForm.password}
                onChange={handleRegistrationChange}
                autoComplete="new-password"
                required
              />
            </label>

            <button type="submit" disabled={isSubmitting}>
              {isSubmitting ? 'Registering...' : 'Register'}
            </button>
          </form>
        )}
      </section>
    </main>
  )
}

export default AuthPage
