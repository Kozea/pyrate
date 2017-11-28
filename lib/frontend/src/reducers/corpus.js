const corpus = (state = [], action) => {
  switch (action.type) {
    case 'ADD_CORPUS':
      return [
        ...state,
        {
          id: action.id,
          title: action.title,
        },
      ]
    default:
      return state
  }
}

export default corpus
