const algorithmes = (state = [], action) => {
  switch (action.type) {
    case 'LOAD_ALGORITHMES_SUCCESS':
      return action.algorithmes.data.algorithmes
    case 'GENERATE_TEXT_SUCCESS':
      return action.text.data.text
    default:
      return state
  }
}

export default algorithmes
