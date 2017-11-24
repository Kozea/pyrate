import React from 'react'
import PropTypes from 'prop-types'
import { connect } from 'react-redux'

import { deleteCat } from '../actions'
// import DeleteCat from '../containers/DeleteCat'

const CategoriesList = ({ categories, btnClick }) => (
  <div>
    {/* {console.log(categories)} */}
    <ul>
      Listes des Catégories ...{categories.map(category => (
        <li key={category.id}>
          {category.label}
          {/* <DeleteCat /> */}
          <button
            onClick={e => {
              e.preventDefault()
              btnClick(category.id)
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

connect(
  function mapStateToProps(state) {
    return { categories: state.categories }
  },
  function mapDispatchToProps(dispatch) {
    return { btnClick: data => dispatch(deleteCat(data)) }
  }
)(CategoriesList)

export default CategoriesList
