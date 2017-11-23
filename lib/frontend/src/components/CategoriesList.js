import React from 'react'
import PropTypes from 'prop-types'
import Category from './Category'

const CategoriesList = ({categories}) => (
  <div>{console.log(categories)}
    <ul>
      {categories.map(category =>
      <li key={category.id}>
        {category.label}
      </li>)}
    </ul>
  </div>

)

CategoriesList.propTypes = {
  categories: PropTypes.arrayOf(PropTypes.shape({
    id: PropTypes.number.isRequired,
    label: PropTypes.string.isRequired
  }).isRequired).isRequired
}


export default CategoriesList
