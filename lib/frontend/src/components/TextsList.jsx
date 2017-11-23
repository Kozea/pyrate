import React from 'react'
import PropTypes from 'prop-types'

const TextsList = ({ texts }) => (
  <div>
    {/* {console.log(texts)} */}
    <ul>
      Listes des Textes générés...{texts.map(text => (
        <li key={text.id}>
          {text.label}
          <button>Supprimer</button>
        </li>
      ))}
    </ul>
  </div>
)

TextsList.propTypes = {
  texts: PropTypes.arrayOf(
    PropTypes.shape({
      category_id: PropTypes.number.isRequired,
      algorithm_id: PropTypes.string.isRequired,
    }).isRequired
  ).isRequired,
}

export default TextsList
