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
        <label>Texts : </label>
        <ul>
          <li>
            <span className="textstitle">
              [Catégorie]Texte généré le 10/10/10 par MonsieurX
            </span>
            <button>Edit</button> <button>Delete</button>
          </li>
          <li>
            <span className="textstitle">
              [Catégorie]Texte généré le 10/01/17 par MonsieurY
            </span>
            <button>Edit</button> <button>Delete</button>
          </li>
          <li>
            <span className="textstitle">
              [Catégorie]Texte généré le 10/08/09 par MonsieurZ
            </span>
            <button>Edit</button> <button>Delete</button>
          </li>
        </ul>
        <button>Generate a new text</button>
      </div>
    )
  }
}

export default Texts
