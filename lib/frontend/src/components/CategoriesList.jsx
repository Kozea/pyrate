import React from 'react'
import { connect } from 'react-redux'

import { deleteCategory, addCategory, editCat, updateCat } from '../actions'

function CategoriesList({ categories, btnClick, addCat, editClick, updCat }) {
  let input
  return (
    <div>
      Liste des Catégories :
      <ul>
        {categories.map(category => (
          <li key={category.id}>
            {category.is_in_edition ? (
              <div>
                <form
                  onSubmit={e => {
                    e.preventDefault()
                    updCat(input.value)
                  }}
                >
                  <input
                    key={input}
                    ref={node => {
                      input = node
                    }}
                  />
                  <button type="submit">Valider</button>
                </form>
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
    return {
      categories: state.categories,
      showEdit: state.showEdit,
    }
  },
  function mapDispatchToProps(dispatch) {
    return {
      btnClick: data => dispatch(deleteCategory(data)),
      addCat: data => dispatch(addCategory(data)),
      updCat: data => dispatch(updateCat(data)),
      editClick: data => dispatch(editCat(data)),
    }
  }
)(CategoriesList)
