import React from 'react'

import AddCategory from '../containers/AddCategory'
import Corpus from '../containers/Corpus'
import DisplayCatList from '../containers/DisplayCategories'
import NavBar from '../containers/NavBar'
import TextGenerator from '../containers/TextGenerator'

export default function App() {
  return (
    <div>
      <NavBar />
      <hr />
      <TextGenerator />
      <hr />
      <hr />
      <DisplayCatList />
      <AddCategory />
      <hr />
      <Corpus />
    </div>
  )
}
