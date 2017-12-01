import pyrateApi from '../pyrateApi'

// CATEGORIES

export function addCategory(catLabel) {
  return function(dispatch) {
    return pyrateApi
      .addCategory(catLabel)
      .then(result => {
        if (result.status === 'fail' || result.status === 'error') {
          dispatch(addCategoryError(result.message))
        } else {
          dispatch(loadCategories())
        }
      })
      .catch(error => {
        throw error
      })
  }
}
export function addCategoryError(message) {
  return { type: 'ADD_ERROR', message }
}

export function deleteCategory(categoryId) {
  return function(dispatch) {
    return pyrateApi
      .deleteCategory(categoryId)
      .then(result => {
        if (result.status === 'fail' || result.status === 'error') {
          dispatch(deleteCategoryError(result.message))
        } else {
          dispatch(deleteCategorySuccess(categoryId, result.message))
        }
      })
      .catch(error => {
        throw error
      })
  }
}

export function deleteCategoryError(message) {
  return { type: 'DEL_ERROR', message }
}
export const deleteCategorySuccess = (categoryId, message) => ({
  type: 'DEL_CATEGORY',
  categoryId: categoryId,
  message: message,
})

export function editCat(categoryId) {
  return {
    type: 'EDIT_CATEGORY',
    categoryId: categoryId,
  }
}

export function loadCategories() {
  return function(dispatch) {
    return pyrateApi
      .getAllCategories()
      .then(categories => {
        if (categories.status === 'fail' || categories.status === 'error') {
          dispatch(loadCategoriesError(categories))
        } else {
          dispatch(loadCategoriesSuccess(categories))
        }
      })
      .catch(error => {
        throw error
      })
  }
}
export function loadCategoriesSuccess(categories) {
  return { type: 'LOAD_CATEGORIES_SUCCESS', categories }
}
export function loadCategoriesError(categories) {
  return { type: 'LOAD_CATEGORIES_ERROR', categories }
}

export function updateCat(categoryId, catLabel) {
  return function(dispatch) {
    return pyrateApi
      .updateCat(categoryId, catLabel)
      .then(result => {
        if (result.status === 'fail' || result.status === 'error') {
          dispatch(updateCategoryError(result.message))
        } else {
          dispatch(updateCatSuccess(categoryId, catLabel, result.message))
        }
      })
      .catch(error => {
        throw error
      })
  }
}
export function updateCategoryError(message) {
  return { type: 'UPD_ERROR', message }
}
export const updateCatSuccess = (categoryId, catLabel, message) => ({
  type: 'UPDATE_CATEGORY',
  categoryId: categoryId,
  catLabel: catLabel,
  message: message,
})

// USERS

function getProfile(dispatch) {
  return pyrateApi
    .getProfile()
    .then(ret => {
      if (ret.status === 'fail' || ret.status === 'error') {
        dispatch(ProfileError(ret.message))
      } else {
        dispatch(ProfileSuccess(ret))
      }
    })
    .catch(error => {
      throw error
    })
}

export function login(email, password) {
  return function(dispatch) {
    return pyrateApi
      .login(email, password)
      .then(ret => {
        if (ret.status === 'fail' || ret.status === 'error') {
          dispatch(AuthError(ret.message))
        } else {
          window.localStorage.setItem('authToken', ret.auth_token)
          getProfile(dispatch)
        }
      })
      .catch(error => {
        throw error
      })
  }
}

export function githubLogin() {
  return function(dispatch) {
    return pyrateApi
      .githubLogin()
      .then(ret => {
        if (ret.status === 'success') {
          window.location = ret.url
        } else {
          dispatch(AuthError(ret.message))
        }
      })
      .catch(error => {
        throw error
      })
  }
}

export function githubCallback(code) {
  return function(dispatch) {
    return pyrateApi
      .githubCallback(code)
      .then(ret => {
        if (ret.status === 'fail' || ret.status === 'error') {
          dispatch(AuthError(ret.message))
        } else {
          window.localStorage.setItem('authToken', ret.auth_token)
          getProfile(dispatch)
        }
      })
      .catch(error => {
        throw error
      })
  }
}

export function register(username, email, password) {
  return function(dispatch) {
    return pyrateApi
      .register(username, email, password)
      .then(ret => {
        if (ret.status === 'fail' || ret.status === 'error') {
          dispatch(AuthError(ret.message))
        } else {
          window.localStorage.setItem('authToken', ret.auth_token)
          getProfile(dispatch)
        }
      })
      .catch(error => {
        throw error
      })
  }
}

export function AuthError(message) {
  return { type: 'AUTH_ERROR', message }
}

export function logout() {
  return { type: 'LOGOUT' }
}

export function loadProfile() {
  if (window.localStorage.getItem('authToken')) {
    return function(dispatch) {
      getProfile(dispatch)
    }
  }
  return { type: 'LOGOUT' }
}

export function ProfileSuccess(message) {
  return { type: 'PROFILE_SUCCESS', message }
}

export function ProfileError(message) {
  return { type: 'PROFILE_ERROR', message }
}

// ALGORITHMS

export function loadAlgorithmes() {
  return function(dispatch) {
    return pyrateApi
      .getAllAlgorithmes()
      .then(algorithmes => {
        if (algorithmes.status === 'fail' || algorithmes.status === 'error') {
          dispatch(loadAlgorithmesError(algorithmes))
        } else {
          dispatch(loadAlgorithmesSuccess(algorithmes))
        }
      })
      .catch(error => {
        throw error
      })
  }
}
export function loadAlgorithmesSuccess(algorithmes) {
  return { type: 'LOAD_ALGORITHMES_SUCCESS', algorithmes }
}
export function loadAlgorithmesError(algorithmes) {
  return { type: 'LOAD_ALGORITHMES_ERROR', algorithmes }
}

export function train(algo, categoryId) {
  return function(dispatch) {
    return pyrateApi
      .train(algo, categoryId)
      .then(text => {
        dispatch(trainSuccess(text))
      })
      .catch(error => {
        throw error
      })
  }
}
export function trainSuccess(generatedText) {
  return { type: 'TRAIN_SUCCESS', generatedText }
}

export function trainInProgress() {
  return { type: 'TRAIN_IN_PROGRESS' }
}

export function generateText(algo, categoryId) {
  return function(dispatch) {
    return pyrateApi
      .generateText(algo, categoryId)
      .then(text => {
        if (text.status === 'fail' || text.status === 'error') {
          dispatch(generateTextError(text.message))
        } else {
          dispatch(generateTextSuccess(text))
        }
      })
      .catch(error => {
        throw error
      })
  }
}
export function generateTextSuccess(generatedText) {
  return { type: 'GENERATE_TEXT_SUCCESS', generatedText }
}

export function generationInProgress() {
  return { type: 'GENERATION_IN_PROGRESS' }
}

export function generateTextError(generatedText) {
  return { type: 'GENERATE_TEXT_ERROR', generatedText }
}

// CORPUS

export function addCorpusTexts(form, catId) {
  return function(dispatch) {
    return pyrateApi
      .addCorpusText(form)
      .then(categories => {
        if (categories.status === 'fail' || categories.status === 'error') {
          dispatch(addCorpusError(categories))
        } else {
          dispatch(loadCorpusTexts(catId))
        }
      })
      .catch(error => {
        throw error
      })
  }
}

export function deleteCorpusTexts(textId, catId) {
  return function(dispatch) {
    return pyrateApi
      .deleteCorpusText(textId)
      .then(texts => {
        if (texts.status === 'fail' || texts.status === 'error') {
          dispatch(deleteCorpusError(texts))
        } else {
          dispatch(loadCorpusTexts(catId))
        }
      })
      .catch(error => {
        throw error
      })
  }
}

export function loadCorpusTexts(catId) {
  return function(dispatch) {
    return pyrateApi
      .getCorpusText(catId)
      .then(categories => {
        if (categories.status === 'fail' || categories.status === 'error') {
          dispatch(loadCorpusError(categories))
        } else {
          dispatch(loadCorpusSuccess(categories))
        }
      })
      .catch(error => {
        throw error
      })
  }
}
export function loadCorpusSuccess(corpusTexts) {
  return { type: 'LOAD_TEXT_SUCCESS', corpusTexts }
}

export function loadCorpusError(corpusTexts) {
  return { type: 'LOAD_TEXT_ERROR', corpusTexts }
}
export function addCorpusError(corpusTexts) {
  return { type: 'ADD_TEXT_ERROR', corpusTexts }
}
export function deleteCorpusError(corpusTexts) {
  return { type: 'DELETE_TEXT_ERROR', corpusTexts }
}
