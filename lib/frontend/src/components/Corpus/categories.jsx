import React from 'react'

class Categories extends React.Component {
  constructor() {
    super()
    this.state = {
      showReply: false,
    }
  }

  render() {
    return (
      <div>
        <label>Catégories : </label>
        <ul>
          <li>
            Romans <button>Modifier</button> <button>Supprimer</button>
          </li>
          <li>
            Articles <button>Modifier</button> <button>Supprimer</button>
          </li>
          <li>
            Rapports <button>Modifier</button> <button>Supprimer</button>
          </li>
        </ul>
        <button>Ajouter une catégorie</button>
      </div>
    )
  }
}

export default Categories
