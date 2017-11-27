const isAuthenticated = (state = false, action) => {
  switch (action.type) {
    case 'LOGIN_SUCCESS':
      console.log(action.message)
      window.localStorage.setItem('authToken', action.message.auth_token)
      return true
    case 'LOGIN_ERROR':
      window.localStorage.removeItem('authToken')
      console.log(action.message)
      return false
    default:
      return state
  }
}

export default isAuthenticated
