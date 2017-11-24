const generatedText = (state = "", action) => {
  switch (action.type) {
    case 'GENERATE_TEXT_SUCCESS':
      console.log("GENERATE_TEXT_SUCCESS")
      console.log(action)
      return action.text.data.text
    case 'GENERATE_TEXT_ERROR':
      console.log("GENERATE_TEXT_ERROR")
      console.log(action.message)
      return action.message
    default:
      return state
  }
}

export default generatedText
