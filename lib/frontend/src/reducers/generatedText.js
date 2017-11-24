const generatedText = (state = "", action) => {
  switch (action.type) {
    case 'GENERATE_TEXT_SUCCESS':
      console.log("GENERATE_TEXT_SUCCESS")
      console.log(action)
      return action.generatedText.data.text
    case 'GENERATE_TEXT_ERROR':
      console.log("GENERATE_TEXT_ERROR")
      console.log(action.generatedText)
      return action.generatedText
    default:
      return state
  }
}

export default generatedText
