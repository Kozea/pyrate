import React from 'react'
import { connect } from 'react-redux'

import { deleteCategory, addCategory, editCat } from '../actions'

function CategoriesList({ categories, btnClick, addCat, showEdit, editClick }) {
  let input
  return (
    <div>
      Liste des Catégories :
      <ul>
        {categories.map(category => (
          <li key={category.id}>
            {showEdit ? (
              <div>
                <input value={category.label} />
                <button type="submit">Valider</button>
              </div>
            ) : (
              <div>
                {category.label}
                <button
                  onClick={e => {
                    e.preventDefault()
                    btnClick(category.id)
                  }}
                >
                  Supprimer
                </button>
              </div>
            )}

            <button
              onClick={e => {
                e.preventDefault()
                editClick()
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
    return {
      categories: state.categories,
      showEdit: state.showEdit,
    }
  },
  function mapDispatchToProps(dispatch) {
    return {
      btnClick: data => dispatch(deleteCategory(data)),
      addCat: data => dispatch(addCategory(data)),
      editClick: data => dispatch(editCat(data)),
    }
  }
)(CategoriesList)
