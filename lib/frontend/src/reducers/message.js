const message = (state = '', action) => {
  switch (action.type) {
    case 'AUTH_ERROR':
      return action.message
    case 'PROFILE_SUCCESS':
      return ''
    case 'LOGIN_ERROR':
      return action.message
    case 'PROFILE_ERROR':
      return action.message
    case 'LOGOUT':
      return ''
    default:
      return state
  }
}

export default message
