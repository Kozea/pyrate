const texts = (state = [], action) => {
  switch (action.type) {
    case 'ADD_TEXT':
      return [
        ...state,
        {
          category_id: action.category_id,
          algorithm_id: action.algorithm_id,
        },
      ]
    default:
      return state
  }
}

export default texts
