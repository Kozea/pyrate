import pyrateApi from '../pyrateApi'

let nextCatId = 0
export const addCategory = (label) => ({
  type: 'ADD_CATEGORY',
  id: nextCatId++,
  label
})

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
