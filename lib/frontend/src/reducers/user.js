const user = (state = null, action) => {
  switch (action.type) {
    case 'PROFILE_SUCCESS':
      return {
        username: action.message.data.username,
        email: action.message.data.email,
        isAdmin: action.message.data.is_admin,
        createdAt: action.message.data.created_at
      }
    case 'PROFILE_ERROR':
      return null
    case 'LOGOUT':
      return null
    default:
      return state
  }
}

export default user
