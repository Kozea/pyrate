import React from 'react'

import NavBar from './NavBar'
import AddCategory from '../containers/AddCategory'
import AddCorpus from '../containers/AddCorpus'
import DisplayCatList from '../containers/DisplayCategories'
import DisplayTextsList from '../containers/DisplayTexts'
import DisplayCorpusList from '../containers/DisplayCorpus'
import TextGenerator from '../containers/TextGenerator'
import DisplayAlgoList from '../containers/DisplayAlgorithmes'

export default function App() {
  return (
    <div>
      <NavBar />
      <hr />
      <TextGenerator />
      <hr />
      <hr />
      <DisplayAlgoList />
      <DisplayCatList />
      <AddCategory />
      <hr />
      <DisplayTextsList />

      <AddCorpus />
      <DisplayCorpusList />
    </div>
  )
}
