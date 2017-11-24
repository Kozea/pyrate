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

export function loadAlgorithmes() {
  return function(dispatch) {
    return pyrateApi.getAllAlgorithmes().then(algorithmes => {
      dispatch(loadAlgorithmesSuccess(algorithmes));
    }).catch(error => {
      throw(error);
    });
  };
}

export function loadAlgorithmesSuccess(algorithmes) {
  return {type: 'LOAD_ALGORITHMES_SUCCESS', algorithmes};
}

export function loadCategories() {
  return function(dispatch) {
    return pyrateApi.getAllCategories().then(categories => {
      dispatch(loadCategoriesSuccess(categories));
    }).catch(error => {
      throw(error);
    });
  };
}

export function loadCategoriesSuccess(categories) {
  return {type: 'LOAD_CATEGORIES_SUCCESS', categories};
}

export function generateText(algo, category_id) {
  return function(dispatch) {
    return pyrateApi.generateText(algo, category_id).then(text => {
      console.log("pyrateApi.generateText")
      console.log("algo")
      console.log(algo)
      console.log("category_id")
      console.log(category_id)
      console.log(text)
      if (text.status === "fail" || text.status === "error") {
        console.log("====================")
        console.log(text)
        dispatch(generateTextError(text.message));
      } else {
        dispatch(generateTextSuccess(text));
      }
    }).catch(error => {
      console.error(error);
      throw(error);
    });
  };
}

export function generateTextSuccess(generatedText) {
  return {type: 'GENERATE_TEXT_SUCCESS', generatedText};
}

export function generateTextError(generatedText) {
  return {type: 'GENERATE_TEXT_ERROR', generatedText};
}
