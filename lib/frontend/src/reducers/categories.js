const categories = (state = [], action) => {
  switch (action.type) {
    case 'ADD_CATEGORY':
      return [
        ...state,
        {
          id: action.id,
          label: action.label
        }
      ]
    default:
      return state
  }
}

export default categories
