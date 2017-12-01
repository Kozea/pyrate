import React from 'react'
import { connect } from 'react-redux'

import { deleteCategory, addCategory, editCat, updateCat } from '../actions'

function CategoriesList({
  user,
  categories,
  btnClick,
  addCat,
  editClick,
  updClick,
}) {
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
                    updClick(category.id, e.target.label.value)
                  }}
                >
                  <input
                    required
                    name="label"
                    key={input}
                    ref={node => {
                      input = node
                    }}
                    defaultValue={category.label}
                  />
                  <button type="submit">Valider</button>
                </form>
              </div>
            ) : (
              <div>
                {category.label}
                {user && (category.owner_id === user.id || user.isAdmin) ? (
                  <button
                    onClick={e => {
                      e.preventDefault()
                      btnClick(category.id)
                    }}
                  >
                    Supprimer
                  </button>
                ) : (
                  ''
                )}
              </div>
            )}
            {user && (category.owner_id === user.id || user.isAdmin) ? (
              <button
                onClick={e => {
                  e.preventDefault()
                  editClick(category.id)
                }}
              >
                {category.is_in_edition ? 'Annuler' : 'Modifier'}
              </button>
            ) : (
              ''
            )}
          </li>
        ))}
      </ul>
      {user !== null && (
        <form
          onSubmit={e => {
            e.preventDefault()
            addCat(input.value)
          }}
        >
          <input
            required
            key={input}
            ref={node => {
              input = node
            }}
          />
          <button type="submit">Ajouter une catégorie</button>
        </form>
      )}
    </div>
  )
}

export default connect(
  function mapStateToProps(state) {
    return {
      categories: state.categories,
      user: state.user,
    }
  },
  function mapDispatchToProps(dispatch) {
    return {
      btnClick: data => dispatch(deleteCategory(data)),
      addCat: data => dispatch(addCategory(data)),
      updClick: (id, data) => dispatch(updateCat(id, data)),
      editClick: data => dispatch(editCat(data)),
    }
  }
)(CategoriesList)
