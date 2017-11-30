const generatedText = (state = '', action) => {
  switch (action.type) {
    case 'TRAIN_SUCCESS':
      return action.generatedText.message
    case 'GENERATE_TEXT_SUCCESS':
      return action.generatedText.data.text
    case 'GENERATE_TEXT_ERROR':
      return action.generatedText
    case 'TRAIN_IN_PROGRESS':
      return 'Training in progress. Please wait.'
    case 'GENERATION_IN_PROGRESS':
      return 'Generation in progress. Please wait.'
    default:
      return state
  }
}

export default generatedText
