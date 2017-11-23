import React from 'react'
import { connect } from 'react-redux'

import { addCorpus } from '../actions'

let AddCorpus = ({ dispatch }) => {
  let input

  return (
    <div>
      <form
        onSubmit={e => {
          e.preventDefault()
          if (!input.value.trim()) {
            return
          }
          dispatch(addCorpus(input.value))
          input.value = ''
        }}
      >
        <input
          ref={node => {
            input = node
          }}
        />
        <button type="submit">Ajouter un document</button>
      </form>
    </div>
  )
}
AddCorpus = connect()(AddCorpus)

export default AddCorpus
