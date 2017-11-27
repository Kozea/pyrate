import React from 'react'
import { connect } from 'react-redux'

import { deleteCategory, addCategory } from '../actions'
// import DeleteCat from '../containers/DeleteCat'

function CategoriesList({ categories, btnClick, addCat }) {
  let input
  return (
    <div>
      Liste des Catégories :
      <ul>
        {categories.map(category => (
          <li key={category.id}>
            {category.label}
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
      <form
        onSubmit={e => {
          e.preventDefault()
          addCat(input.value)
        }}
      >
        <input
          key={input}
          ref={node => {
            input = node
          }}
        />
        <button type="submit">Ajouter une catégorie</button>
      </form>
    </div>
  )
}

export default connect(
  function mapStateToProps(state) {
    return { categories: state.categories }
  },
  function mapDispatchToProps(dispatch) {
    return {
      btnClick: data => dispatch(deleteCategory(data)),
      addCat: data => dispatch(addCategory(data)),
    }
  }
)(CategoriesList)
