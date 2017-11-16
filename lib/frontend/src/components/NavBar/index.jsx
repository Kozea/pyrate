import React from 'react'
import Login from '../User/login'
import Register from '../User/register'
import Categories from '../Corpus/categories'
import Corpus from '../Corpus/corpustexts'
import Texts from '../Corpus/texts'

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
      case '/categories':
        return <Categories />
      case '/corpustexts':
        return <Corpus />
      case '/texts':
        return <Texts />
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
