import React from 'react'
import { connect } from 'react-redux'

import { deleteCat } from '../actions'
import CategoriesList from '../components/CategoriesList'

let DeleteCat = ({ dispatch }) => {
  return (
    <div>
      <button
        onSubmit={e => {
          e.preventDefault()
          dispatch(deleteCat)
        }}
      >
        Supprimer
      </button>
    </div>
  )
}
DeleteCat = connect(
  function mapStateToProps(state) {
    return { categories: state.categories }
  },
  function mapDispatchToProps(dispatch) {
    return { deleteCat: data => dispatch(deleteCat(data)) }
  }
)(DeleteCat)

export default DeleteCat
