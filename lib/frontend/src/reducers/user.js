const user = (state = null, action) => {
  switch (action.type) {
    case 'AUTH_ERROR':
      window.localStorage.removeItem('authToken')
      return null
    case 'PROFILE_SUCCESS':
      return {
        username: action.message.data.username,
        email: action.message.data.email,
        isAdmin: action.message.data.is_admin,
        createdAt: action.message.data.created_at,
      }
    case 'PROFILE_ERROR':
      window.localStorage.removeItem('authToken')
      return null
    case 'LOGOUT':
      window.localStorage.removeItem('authToken')
      return null
    default:
      return state
  }
}

export default user
