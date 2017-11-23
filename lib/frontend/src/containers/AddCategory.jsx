import React from 'react'
import { connect } from 'react-redux'

import { addCategory } from '../actions'

let AddCategory = ({ dispatch }) => {
  let input

  return (
    <div>
      <form
        onSubmit={e => {
          e.preventDefault()
          if (!input.value.trim()) {
            return
          }
          dispatch(addCategory(input.value))
          input.value = ''
        }}
      >
        <input
          ref={node => {
            input = node
          }}
        />
        <button type="submit">Ajouter une catégorie</button>
      </form>
    </div>
  )
}
AddCategory = connect()(AddCategory)

export default AddCategory