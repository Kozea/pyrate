import React from 'react'

class Texts extends React.Component {
  constructor() {
    super()
    this.state = {
      showReply: false,
    }
  }

  render() {
    return (
      <div>
        <label>Textes : </label>
        <ul>
          <li>
            <span className="textstitle">
              [Catégorie]Texte généré le 10/10/10 par MonsieurX
            </span>
            <button>Editer</button> <button>Supprimer</button>
          </li>
          <li>
            <span className="textstitle">
              [Catégorie]Texte généré le 10/01/17 par MonsieurY
            </span>
            <button>Editer</button> <button>Supprimer</button>
          </li>
          <li>
            <span className="textstitle">
              [Catégorie]Texte généré le 10/08/09 par MonsieurZ
            </span>
            <button>Editer</button> <button>Supprimer</button>
          </li>
        </ul>
        <button>Générer un nouveau texte</button>
      </div>
    )
  }
}

export default Texts
