import React from 'react'

import NavBar from './Navbar'
import Content from './Content'
import Login from './User/login'
import Register from './User/register'
import Categories from './Corpus/categories'
import Corpus from './Corpus/corpustexts'
import Texts from './Corpus/texts'
import '../style.css'

class App extends React.Component {
  constructor() {
    super()
    this.state = {
      showReply: false,
    }
  }

  renderRoute() {
    switch (window.location.pathname) {
      case '/':
        return <Content />
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
      <div className="app">
        <NavBar />
        {this.renderRoute()}
      </div>
    )
  }
}

export default App
