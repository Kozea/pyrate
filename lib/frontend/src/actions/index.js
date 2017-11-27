import pyrateApi from '../pyrateApi'

let nextCatId = 0
export const addCategory = label => ({
  type: 'ADD_CATEGORY',
  id: nextCatId++,
  label,
})

let nextCoId = 0
export const addCorpus = title => ({
  type: 'ADD_CORPUS',
  id: nextCoId++,
  title,
})

export const deleteCat = label => ({
  type: 'DEL_CATEGORY',
  id: nextCatId--,
  label: label--,
})

export function login(email, password) {
  return function (dispatch) {
    return pyrateApi.login(email, password).then(ret => {
      if (ret.status === 'fail' || ret.status === 'error') {
        dispatch(AuthError(ret.message))
      } else {
        dispatch(AuthSuccess(ret))
      }
    }).catch(error => {
      throw (error)
    })
  }
}

export function register(username, email, password) {
  return function (dispatch) {
    return pyrateApi.register(username, email, password).then(ret => {
      if (ret.status === 'fail' || ret.status === 'error') {
        dispatch(AuthError(ret.message))
      } else {
        dispatch(AuthSuccess(ret))
      }
    }).catch(error => {
      throw (error)
    })
  }
}

export function AuthSuccess(message) {
  return { type: 'LOGIN_SUCCESS', message }
}

export function AuthError(message) {
  return { type: 'LOGIN_ERROR', message }
}

export function isLogged() {
  const tokenExists = window.localStorage.getItem('authToken') !== null
  return { type: 'INIT', tokenExists }
}

export function logout() {
  return { type: 'LOGOUT' }
}

export function loadAlgorithmes() {
  return function(dispatch) {
    return pyrateApi.getAllAlgorithmes().then(algorithmes => {
      dispatch(loadAlgorithmesSuccess(algorithmes))
    }).catch(error => {
      throw (error)
    })
  }
}

export function loadAlgorithmesSuccess(algorithmes) {
  return { type: 'LOAD_ALGORITHMES_SUCCESS', algorithmes }
}

export function loadCategories() {
  return function(dispatch) {
    return pyrateApi.getAllCategories().then(categories => {
      dispatch(loadCategoriesSuccess(categories))
    }).catch(error => {
      throw (error)
    })
  }
}

export function loadCategoriesSuccess(categories) {
  return { type: 'LOAD_CATEGORIES_SUCCESS', categories }
}


export function train(algo, categoryId) {
  return function(dispatch) {
    return pyrateApi.train(algo, categoryId).then(text => {
      dispatch(trainSuccess(text))
    }).catch(error => {
      throw (error)
    })
  }
}

export function trainSuccess(generatedText) {
  return { type: 'TRAIN_SUCCESS', generatedText }
}

export function generateText(algo, categoryId) {
  return function(dispatch) {
    return pyrateApi.generateText(algo, categoryId).then(text => {
      if (text.status === 'fail' || text.status === 'error') {
        dispatch(generateTextError(text.message))
      } else {
        dispatch(generateTextSuccess(text))
      }
    }).catch(error => {
      throw (error)
    })
  }
}

export function generateTextSuccess(generatedText) {
  return { type: 'GENERATE_TEXT_SUCCESS', generatedText }
}

export function generateTextError(generatedText) {
  return { type: 'GENERATE_TEXT_ERROR', generatedText }
}
