const algorithmes = (state = [], action) => {
  switch (action.type) {
    case 'LOAD_ALGORITHMES_SUCCESS':
      return action.algorithmes.data.algorithmes
    default:
      return state
  }
}

export default algorithmes