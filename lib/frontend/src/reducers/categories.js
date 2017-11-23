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
      return state.filter(({ id }) => id !== action.data)
    default:
      return state
  }
}

export default categories
