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
        <br />
        <button>Générer</button>
        <br />
        <label>Résultat : </label>
        <br />
        <output />
        <button>Sauvegarder</button>
      </div>
    )
  }
}

export default Content
