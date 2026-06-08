import { useState } from 'react'
import {
  loginUser,
  registerUser,
  requestPasswordReset,
  resetPassword,
} from '../api/auth.js'
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

const initialForgotPasswordForm = {
  email: '',
}

const initialResetPasswordForm = {
  token: new URLSearchParams(window.location.search).get('reset_token') || '',
  password: '',
}

function AuthPage({ onAuthenticated }) {
  const [mode, setMode] = useState(
    initialResetPasswordForm.token ? 'reset-password' : 'login',
  )
  const [loginForm, setLoginForm] = useState(initialLoginForm)
  const [registrationForm, setRegistrationForm] = useState(
    initialRegistrationForm,
  )
  const [forgotPasswordForm, setForgotPasswordForm] = useState(
    initialForgotPasswordForm,
  )
  const [resetPasswordForm, setResetPasswordForm] = useState(
    initialResetPasswordForm,
  )
  const [errorMessage, setErrorMessage] = useState('')
  const [successMessage, setSuccessMessage] = useState('')
  const [isSubmitting, setIsSubmitting] = useState(false)

  const isLogin = mode === 'login'
  const isRegister = mode === 'register'
  const isForgotPassword = mode === 'forgot-password'
  const isResetPassword = mode === 'reset-password'

  function getTitle() {
    if (isRegister) {
      return 'Register'
    }

    if (isForgotPassword) {
      return 'Forgot password'
    }

    if (isResetPassword) {
      return 'Reset password'
    }

    return 'Login'
  }

  function changeMode(nextMode) {
    setMode(nextMode)
    setErrorMessage('')
    setSuccessMessage('')
  }

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

  function handleForgotPasswordChange(event) {
    const { name, value } = event.target
    setForgotPasswordForm((currentForm) => ({
      ...currentForm,
      [name]: value,
    }))
  }

  function handleResetPasswordChange(event) {
    const { name, value } = event.target
    setResetPasswordForm((currentForm) => ({
      ...currentForm,
      [name]: value,
    }))
  }

  async function handleSubmit(event) {
    event.preventDefault()
    setErrorMessage('')
    setSuccessMessage('')
    setIsSubmitting(true)

    try {
      if (isForgotPassword) {
        const response = await requestPasswordReset(forgotPasswordForm)
        setSuccessMessage(response.message)
        return
      }

      if (isResetPassword) {
        const response = await resetPassword(resetPasswordForm)
        setMode('login')
        setSuccessMessage(response.message)
        setResetPasswordForm({
          token: '',
          password: '',
        })
        return
      }

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
          <h1 id="auth-title">{getTitle()}</h1>
        </div>

        <div className="auth-tabs" aria-label="Authentication options">
          <button
            type="button"
            className={isLogin ? 'active' : ''}
            onClick={() => changeMode('login')}
          >
            Login
          </button>
          <button
            type="button"
            className={isRegister ? 'active' : ''}
            onClick={() => changeMode('register')}
          >
            Register
          </button>
        </div>

        {errorMessage && <p className="auth-error">{errorMessage}</p>}
        {successMessage && <p className="auth-success">{successMessage}</p>}

        {isLogin && (
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

            <button
              type="button"
              className="auth-link-button"
              onClick={() => changeMode('forgot-password')}
            >
              Forgot password?
            </button>
          </form>
        )}

        {isRegister && (
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

        {isForgotPassword && (
          <form className="auth-form" onSubmit={handleSubmit}>
            <label>
              Email
              <input
                name="email"
                type="email"
                value={forgotPasswordForm.email}
                onChange={handleForgotPasswordChange}
                autoComplete="email"
                required
              />
            </label>

            <button type="submit" disabled={isSubmitting}>
              {isSubmitting ? 'Sending...' : 'Send reset link'}
            </button>

            <button
              type="button"
              className="auth-link-button"
              onClick={() => changeMode('login')}
            >
              Back to login
            </button>
          </form>
        )}

        {isResetPassword && (
          <form className="auth-form" onSubmit={handleSubmit}>
            <label>
              Reset token
              <input
                name="token"
                type="text"
                value={resetPasswordForm.token}
                onChange={handleResetPasswordChange}
                required
              />
            </label>

            <label>
              New password
              <input
                name="password"
                type="password"
                value={resetPasswordForm.password}
                onChange={handleResetPasswordChange}
                autoComplete="new-password"
                required
              />
            </label>

            <button type="submit" disabled={isSubmitting}>
              {isSubmitting ? 'Resetting...' : 'Reset password'}
            </button>

            <button
              type="button"
              className="auth-link-button"
              onClick={() => changeMode('login')}
            >
              Back to login
            </button>
          </form>
        )}
      </section>
    </main>
  )
}

export default AuthPage
