// composant d'affichage , il affiche le sous-composant 'categorie' +sieurs fois

import React from 'react'
import { connect } from 'react-redux'

import { updateForm, addCat } from '../actions'
import Categorie from './categorie'
import CatForm from './CatForm'

let Categories = props => {
  const { categories, addCat, updateForm } = props
  console.log(categories)
  console.log(addCat)
  console.log(updateForm)

  return (
    <div>
      <label>Catégories : </label>
      {/* // on boucle sur la liste des categories et on appelle 'Categorie' */}
      <ul>
        {categories.reducer.map(categorie => (
          <li key={categorie.get('id')}>
            <Categorie item={categorie.toJS()} />
          </li>
        ))}
      </ul>
      <hr />
      <label>Ajouter une catégorie</label>
      {/* On affiche le formulaire d'ajout */}
      <CatForm
        key="new"
        formKey="new"
        saveForm={addCat}
        updateForm={updateForm}
      />
    </div>
  )
}

// container: on lie le comp parent qui est categories à redux.
// mapStateToProps prend l'etat et le transmet à la liste des categories ss
// forme de proprietes.
// mapDispatchToProps est la fct chargé de faire le lien entre les proprietes
// aux fonctions issues de actions.js
Categories = connect(
  function mapStateToProps(state) {
    return { students: state }
  },
  function mapDispatchToProps(dispatch) {
    return {
      updateForm: data => dispatch(updateForm(data)),
      addStudent: data => dispatch(addCat(data)),
    }
  }
)(Categories)

export default Categories
