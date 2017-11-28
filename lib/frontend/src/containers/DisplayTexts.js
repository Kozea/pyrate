import { connect } from 'react-redux'

import TextsList from '../components/TextsList'

const DisplayTextsList = connect(
  function mapStateToProps(state) {
    return { texts: state.texts }
  },
  function mapDispatchToProps(/* {dispatch} */) {
    return {}
  }
)(TextsList)

export default DisplayTextsList
