import React from 'react'

class NavBar extends React.Component {
  constructor() {
    super()
    this.state = {
      showReply: false,
    }
  }

  render() {
    return (
      <header>
        <h1>PyRaTe</h1>
        <ul id="menu_horizontal">
          <li className="bouton_gauche">
            <a href="/">Accueil</a>
          </li>
          <li className="bouton_gauche">
            <a href="/texts">Textes</a>
          </li>
          <li className="bouton_gauche">
            <a href="/corpustexts">Corpus</a>
          </li>
          <li className="bouton_gauche">
            <a href="/categories">Catégories</a>
          </li>
          <li className="bouton_droite">
            <a href="/login">Se connecter</a>
          </li>
          <li className="bouton_droite">
            <a href="/register">S&apos;inscrire</a>
          </li>
        </ul>
      </header>
    )
  }
}

export default NavBar
