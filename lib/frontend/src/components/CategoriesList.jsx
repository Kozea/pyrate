import React from 'react'
import PropTypes from 'prop-types'

import { deleteCat } from '../actions'
// import Category from './Category'

const CategoriesList = ({ categories }) => (
  <div>
    {/* {console.log(categories)} */}
    <ul>
      Listes des Catégories ...{categories.map(category => (
        <li key={category.id}>
          {category.label}
          <button
            onClick={() => {
              deleteCat(category)
            }}
          >
            Supprimer
          </button>
        </li>
      ))}
    </ul>
  </div>
)

CategoriesList.propTypes = {
  categories: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number.isRequired,
      label: PropTypes.string.isRequired,
    }).isRequired
  ).isRequired,
}

export default CategoriesList
