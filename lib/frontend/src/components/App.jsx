import React from 'react'

import NavBar from './NavBar'
import AddCategory from '../containers/AddCategory.js'
import DisplayCatList from '../containers/DisplayCategories.js'

export default function App() {
  return (
    <div>
      <NavBar />
      <AddCategory />
      <DisplayCatList />
    </div>
  )
}
