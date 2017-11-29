const message = (state = '', action) => {
  switch (action.type) {
    case 'AUTH_ERROR':
    case 'LOGIN_ERROR':
    case 'PROFILE_ERROR':
    case 'DEL_ERROR':
    case 'UPD_ERROR':
    case 'ADD_ERROR':
      return action.message
    case 'ADD_TEXT_ERROR':
    case 'DELETE_TEXT_ERROR':
      return action.corpusTexts.message
    case 'PROFILE_SUCCESS':
    case 'LOGOUT':
      return ''
    default:
      return state
  }
}

export default message
