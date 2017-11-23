import React from 'react'

import NavBar from './NavBar'
import AddCategory from '../containers/AddCategory'
import AddCorpus from '../containers/AddCorpus'
import DisplayCatList from '../containers/DisplayCategories'
import DisplayTextsList from '../containers/DisplayTexts'
import DisplayCorpusList from '../containers/DisplayCorpus'
import TextGenerator from '../containers/DisplayTextGenerator'

export default function App() {
  return (
    <div>
      <NavBar />
      <hr />
      <TextGenerator />
      <hr />
      <AddCategory />
      <DisplayCatList />
      <hr />
      <DisplayTextsList />

      <AddCorpus />
      <DisplayCorpusList />
    </div>
  )
}
