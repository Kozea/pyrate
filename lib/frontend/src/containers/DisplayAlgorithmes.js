import { connect } from 'react-redux'

import AlgorithmesList from '../components/AlgorithmesList'

const DisplayAlgoList = connect(
  function mapStateToProps(state) {
    return { algorithmes: state.algorithmes }
  },
  function mapDispatchToProps(/* {dispatch} */) {
    return {}
  }
)(AlgorithmesList)

export default DisplayAlgoList
