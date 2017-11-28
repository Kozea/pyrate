const corpusTexts = (state = [], action) => {
  switch (action.type) {
    case 'LOAD_TEXT_SUCCESS':
      return action.corpusTexts.data.texts
    case 'LOAD_TEXT_ERROR':
    default:
      return state
  }
}

export default corpusTexts
