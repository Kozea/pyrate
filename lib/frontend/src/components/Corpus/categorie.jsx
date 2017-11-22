import React from 'react'

import CatForm from './CatForm'

const Categorie = props => {
  // item contient les infos de catégorie (id, catName)
  // updateForm est une fct d'evenement
  const { item, updateForm } = props

  return (
    <span>
      <div>
        {item.catName}
        <input type="checkbox" id={item.id} />
        {item.isVisible ? (
          <CatForm
            key={item.id}
            formKey={String(item.id)}
            initialValues={item}
            saveForm={updateForm}
          />
        ) : null}
      </div>
    </span>
  )
}
export default Categorie
