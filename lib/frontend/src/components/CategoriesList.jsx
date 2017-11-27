import React from 'react'
import { connect } from 'react-redux'

import { deleteCategory, addCategory, updateCategory } from '../actions'

function CategoriesList({ categories, btnClick, editClick, addCat }) {
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
            <button
              onClick={e => {
                e.preventDefault()
                editClick(category.id)
              }}
            >
              Modifer
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
      editClick: data => dispatch(updateCategory(data)),
      addCat: data => dispatch(addCategory(data)),
    }
  }
)(CategoriesList)
