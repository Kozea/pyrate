import React from 'react'
import NavBar from './NavBar'
import Content from './Content'

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
    }
  }

  render() {
    return (
      <div>
        <NavBar />
        {this.renderRoute()}
      </div>
    )
  }
}

export default App
