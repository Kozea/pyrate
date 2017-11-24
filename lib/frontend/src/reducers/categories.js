const categories = (state = [], action) => {
  switch (action.type) {
    case 'ADD_CATEGORY':
      return [
        ...state,
        {
          id: action.id,
          label: action.label,
        },
      ]
    case 'DEL_CATEGORY':
      return [delete state[action.id]]
    default:
      return state
  }
}

export default categories
