import React from 'react'

// import AddCategory from '../containers/AddCategory'
import Corpus from '../containers/Corpus'
import CategoriesList from '../components/CategoriesList'
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
      <CategoriesList />
      <hr />
      <Corpus />
    </div>
  )
}
