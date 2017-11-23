import { connect } from 'react-redux'

import CorpusList from '../components/CorpusList'

const DisplayCorpusList = connect(
  function mapStateToProps(state) {
    return { corpus: state.corpus }
  },
  function mapDispatchToProps(/* {dispatch} */) {
    return {}
  }
)(CorpusList)

export default DisplayCorpusList
