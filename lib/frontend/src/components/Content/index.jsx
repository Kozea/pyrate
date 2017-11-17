import React from 'react'

class Content extends React.Component {
  constructor() {
    super()
    this.state = {
      showReply: false,
    }
  }

  render() {
    return (
      <div className="content">
        <label>Catégorie : </label>
        <select>
          <option>Rapports de stage</option>
          <option>Lettres de motivation</option>
        </select>
        <button>Valider</button>
        <br />
        <button>Générer</button>
        <br />
        <label>Résultat : </label>
        <br />
        <output />
        <button>Sauvegarder</button>
        <br />
        <label>Derniers textes générés : </label>
        <select>
          <option>Texte généré le 01/10/17</option>
          <option> ... </option>
        </select>
      </div>
    )
  }
}

export default Content
