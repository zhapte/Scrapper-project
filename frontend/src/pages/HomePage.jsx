import './HomePage.css'

function HomePage({ user, onLogout }) {
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
        <h2>Welcome, {user.firstName}</h2>
        <p>{user.email}</p>
      </section>
    </main>
  )
}

export default HomePage
