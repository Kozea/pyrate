const categories = (state = [], action) => {
  switch (action.type) {
    case 'ADD_CATEGORY':
      return [
        ...state,
        {
          id: action.id,
          label: action.catLabel,
          owner_id: action.owner_id,
        },
      ]
    case 'EDIT_CATEGORY':
      return state.map(category => ({
        ...category,
        is_in_edition:
          category.id === action.categoryId
            ? !category.is_in_edition
            : category.is_in_edition,
      }))

    case 'LOAD_CATEGORIES_SUCCESS':
      return action.categories.data.categories.map(category => ({
        id: category.id,
        label: category.label,
        owner_id: category.owner_id,
        owner_username: category.owner_username,
        is_in_edition: false,
      }))
    case 'DEL_CATEGORY':
      return state.filter(category => category.id !== action.categoryId)
    case 'LOAD_CATEGORIES_ERROR':
      return state
    case 'UPDATE_CATEGORY':
      return state.map(category => ({
        ...category,
        label:
          category.id === action.categoryId ? action.catLabel : category.label,
        is_in_edition:
          category.id === action.categoryId
            ? !category.is_in_edition
            : category.is_in_edition,
      }))
    case 'DEL_ERROR':
    case 'UPD_ERROR':
    case 'ADD_ERROR':
      return action.message
    default:
      return state
  }
}

export default categories
