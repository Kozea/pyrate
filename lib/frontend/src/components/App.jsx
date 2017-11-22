import React from 'react'
import { connect } from 'react-redux'

import { menu } from './actions'
import NavBar from './Navbar'

import '../style.css'

class App extends React.Component {
  constructor() {
    super()
    this.state = {
      showReply: false,
    }
  }
  render() {
    return (
      <div className="app">
        <NavBar />
        <div
          value={menu}
          onChange={e => onClickComp()}>
      </div>
    )
  }
}
{/* // container: on lie le comp parent à redux.
// mapStateToProps prend l'etat et le transmet à la liste des categories ss
// forme de proprietes.
// mapDispatchToProps est la fct chargé de faire le lien entre les proprietes
// aux fonctions issues de actions.js */}

export default connect(
  state => ({ menu: state.menu }),
  dispatch => ({
    onClickComp: value => {
      dispatch(menu(value))
    },
  })
)(App)
