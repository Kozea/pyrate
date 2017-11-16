import React from 'react'
import Login from '../User/login'
import Register from '../User/register'

class NavBar extends React.Component {
  constructor() {
    super()
    this.state = {
      showReply: false,
    }
  }

  renderRoute() {
    switch (window.location.pathname) {
      case '/login':
        return <Login />
      case '/register':
        return <Register />
    }
  }

  render() {
    return (
      <div className="navbar">
        <h1>PyRaTe</h1>
        <button onClick={() => (window.location.href = '/login')}>Login</button>
        <button onClick={() => (window.location.href = '/register')}>
          Register
        </button>
        {this.renderRoute()}
      </div>
    )
  }
}

export default NavBar
