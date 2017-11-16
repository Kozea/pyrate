import React from 'react'

class Corpus extends React.Component {
  constructor() {
    super()
    this.state = {
      showReply: false,
    }
  }

  render() {
    return (
      <div>
        <label>Corpus : </label>
        <ul>
          <li>
            <span className="corpustitle">Les Misérables, de Victor HUGO</span>
            <button>Modifier</button> <button>Supprimer</button>
          </li>
          <li>
            <span className="corpustitle">etcc</span>
            <button>Modifier</button> <button>Supprimer</button>
          </li>
          <li>
            <span className="corpustitle">etcccc</span>
            <button>Modifier</button> <button>Supprimer</button>
          </li>
        </ul>
        <button>Ajouter un document</button>
      </div>
    )
  }
}

export default Corpus
