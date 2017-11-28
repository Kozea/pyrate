import { connect } from 'react-redux'

import CategoriesList from '../components/CategoriesList'
// import { addCategory } from '../actions'

const DisplayCatList = connect(
  function mapStateToProps(state) {
    return { categories: state.categories }
  },
  function mapDispatchToProps(/* {dispatch} */) {
    return {}
  }
)(CategoriesList)

export default DisplayCatList
