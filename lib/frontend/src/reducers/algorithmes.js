const algorithmes = (state = [], action) => {
  switch (action.type) {
    case 'LOAD_ALGORITHMES_SUCCESS':
      return action.algorithmes.data.algorithmes
    case 'LOAD_ALGORITHMES_ERROR':
    default:
      return state
  }
}

export default algorithmes
