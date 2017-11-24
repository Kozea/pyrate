const algorithmes = (state = [], action) => {
  switch (action.type) {
    case 'LOAD_ALGORITHMES_SUCCESS':
      console.log("LOAD_ALGORITHMES_SUCCESS")
      console.log(action)
      return action.algorithmes.data.algorithmes
    default:
      return state
  }
}

export default algorithmes
