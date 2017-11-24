import { connect } from 'react-redux'

import TextGenerator from '../components/TextGenerator'

const DisplayTextGenerator = connect(
  function mapStateToProps(state) {
    return {
      algorithmes: state.algorithmes,
      categories: state.categories,
      text: state.generatedText,
    }
  },
  function mapDispatchToProps(/* {dispatch} */) {
    return {}
  },
)(TextGenerator)

export default DisplayTextGenerator
