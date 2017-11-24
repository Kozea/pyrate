const generatedText = (state = "", action) => {
  switch (action.type) {
    case 'GENERATE_TEXT_SUCCESS':
      return action.generatedText.data.text
    case 'GENERATE_TEXT_ERROR':
      return action.generatedText
    default:
      return state
  }
}

export default generatedText
