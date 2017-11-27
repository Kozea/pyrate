import React from 'react'

import NavBar from '../containers/NavBar'
import AddCorpus from '../containers/AddCorpus'
import DisplayCatList from '../containers/DisplayCategories'
import DisplayTextsList from '../containers/DisplayTexts'
import DisplayCorpusList from '../containers/DisplayCorpus'
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
      <hr />
      <DisplayTextsList />

      <AddCorpus />
      <DisplayCorpusList />
    </div>
  )
}
