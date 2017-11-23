import { connect } from 'react-redux'

import AlgorithmesList from '../components/Algorithm'

const DisplayAlgoList = connect(
  function mapStateToProps(state) {
    return { algorithmes: state.algorithmes }
  },
  function mapDispatchToProps(/* {dispatch} */) {
    return {}
  }
)(AlgorithmesList)

export default DisplayAlgoList
