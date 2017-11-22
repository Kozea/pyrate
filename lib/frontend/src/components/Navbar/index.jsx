import React from 'react'
import ReactDom from 'react-dom'

import Content from '../Content'
import Login from '../User/login'
import Register from '../User/register'
import Categories from '../Corpus/categories'
import Corpus from '../Corpus/corpustexts'
import Texts from '../Corpus/texts'

export default class NavBar extends React.Component {
  constructor() {
    super()
    this.state = {
      showReply: false,
    }
    this.handleClick = this.handleClick.bind(this)
  }
  handleClick() {
    this.props.dispatch(clickComp())
  }
  render() {
    return (
      <header>
        <h1>PyRaTe</h1>
        <ul id="menu_horizontal">
          <li className="bouton_gauche">
            <button onClick={this.handleClick}>Accueil</button>
          </li>
          <li className="bouton_gauche">
            <button onClick={this.handleClick}>Textes</button>
          </li>
          <li className="bouton_gauche">
            <button>Corpus</button>
          </li>
          <li className="bouton_gauche">
            <button
              onClick={() =>
                ReactDom.render(
                  <Categories />,
                  document.getElementById('corps')
                )
              }
            >
              Catégories
            </button>
          </li>
          <li className="bouton_droite">
            <button
              onClick={() =>
                ReactDom.render(<Login />, document.getElementById('corps'))
              }
            >
              Se connecter
            </button>
          </li>
          <li className="bouton_droite">
            <button
              onClick={() =>
                ReactDom.render(<Register />, document.getElementById('corps'))
              }
            >
              S&apos;inscrire
            </button>
          </li>
        </ul>
      </header>
    )
  }
}
