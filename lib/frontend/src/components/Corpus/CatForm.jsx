import React from 'react'
import PropTypes from 'prop-types'
import { reduxForm } from 'redux-form'

// fonction de validation contenant des règles
const validate = values => {
  const errors = {}

  if (!values.catName) {
    errors.catName = 'un nom est requis'
  } else if (values.catName.length < 3) {
    errors.catName = "le nom donné doit être d'au moins 3 caractères"
  }
  return errors
}
let CatForm = props => {
  const save = data => {
    saveForm(data)
    if (!id.value) {
      resetForm()
    }
  }

  const {
    fields: { id, catName, isUpdated },
    // handleSubmit & resetForm sont 2 fcts natives de reduxForm
    handleSubmit,
    resetForm,
    saveForm,
  } = props

  return (
    <form onSubmit={handleSubmit(save)}>
      <div>
        <label>Catégorie</label>
      </div>
      <div>
        <input type="text" placeholder="donnez une catégorie" {...catName} />
      </div>
      {catName.touched && catName.error && <div>{catName.error}</div>}
      {isUpdated.value ? <div>Modification enregistrée</div> : null}
    </form>
  )
}

CatForm.propTypes = {
  fields: PropTypes.object.isRequired,
  handleSubmit: PropTypes.func.isRequired,
  saveForm: PropTypes.func.isRequired,
}

// Rattachement du composant CatForm à reduxForm.. ce qui permet a redux de
// gerer l'etat
CatForm = reduxForm({
  form: 'categorie',
  fields: ['id', 'catName', 'isVisible', 'isUpdated'],
  validate,
})(CatForm)

export default CatForm
