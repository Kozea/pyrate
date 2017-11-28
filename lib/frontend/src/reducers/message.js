const message = (state = '', action) => {
  switch (action.type) {
    case 'AUTH_ERROR':
    case 'LOGIN_ERROR':
    case 'PROFILE_ERROR':
      return action.message
    case 'PROFILE_SUCCESS':
    case 'LOGOUT':
      return ''
    default:
      return state
  }
}

export default message
