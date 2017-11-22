let nextCatId = 0
export const addCategory = (label) => ({
  type: 'ADD_CATEGORY',
  id: nextCatId++,
  label
})
