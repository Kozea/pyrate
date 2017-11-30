import React from 'react'
import PropTypes from 'prop-types'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'

import {
  train,
  generateText,
  trainInProgress,
  generationInProgress,
} from '../actions'

class TextGenerator extends React.Component {
  constructor(props, context) {
    super(props, context)
    this.state = {
      algorithmes: this.props.algorithmes,
      categories: this.props.categories,
      text: this.props.generatedText,
      selectedAlgo: '',
      selectedCategory: '',
      isDisabled: false,
    }
  }

  componentWillReceiveProps(nextProps) {
    const selectedAlgo = nextProps.algorithmes[0]
      ? nextProps.algorithmes[0].label
      : ''
    const selectedCategory = nextProps.categories[0]
      ? nextProps.categories[0].id
      : ''

    if (this.props.algorithmes !== nextProps.algorithmes) {
      this.setState({
        algorithmes: nextProps.algorithmes,
        selectedAlgo: selectedAlgo,
      })
    }
    if (this.props.categories !== nextProps.categories) {
      this.setState({
        categories: nextProps.categories,
        selectedCategory: selectedCategory,
      })
    }

    if (nextProps.text.match(/Please wait/g)) {
      this.setState({ isDisabled: true })
    } else {
      this.setState({ isDisabled: false })
    }
    if (this.props.text !== nextProps.text) {
      this.setState({ text: nextProps.text })
    }
  }

  handleAlgoChange(event) {
    this.setState({ selectedAlgo: event.target.value, text: '' })
  }
  handleCatChange(event) {
    this.setState({ selectedCategory: event.target.value, text: '' })
  }

  formPreventDefault(event) {
    event.preventDefault()
  }

  runGenText(event, type) {
    event.preventDefault()
    const catId = parseInt(this.state.selectedCategory)
    switch (type) {
      case 'generate':
        this.props.actions.generationInProgress()
        this.props.actions.generateText(this.state.selectedAlgo, catId)
        break
      default:
        this.props.actions.trainInProgress()
        this.props.actions.train(this.state.selectedAlgo, catId)
    }
  }

  render() {
    return (
      <div>
        <form onSubmit={event => this.formPreventDefault(event)}>
          Algorithmes displonibles :
          <select name="algo" onChange={event => this.handleAlgoChange(event)}>
            {this.state.algorithmes.map(algorithm => (
              <option key={algorithm.id} value={algorithm.label}>
                {algorithm.label}
              </option>
            ))}
          </select>
          Catégories :
          <select name="cat" onChange={event => this.handleCatChange(event)}>
            {this.state.categories.map(category => (
              <option key={category.id} value={category.id}>
                {category.label}
              </option>
            ))}
          </select>
          <button
            onClick={event => this.runGenText(event, 'train')}
            disabled={this.state.isDisabled}
          >
            Train
          </button>
          <button
            onClick={event => this.runGenText(event, 'generate')}
            disabled={this.state.isDisabled}
          >
            Generate
          </button>
          <br />
          <textarea
            name="message"
            rows="15"
            cols="100"
            value={this.state.text}
          />
        </form>
      </div>
    )
  }
}

function mapStateToProps(state) {
  return {
    algorithmes: state.algorithmes,
    categories: state.categories,
    text: state.generatedText,
  }
}
function mapDispatchToProps(dispatch) {
  return {
    actions: bindActionCreators(
      { train, generateText, trainInProgress, generationInProgress },
      dispatch
    ),
  }
}

TextGenerator.propTypes = {
  actions: PropTypes.object.isRequired,
  algorithmes: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number.isRequired,
      label: PropTypes.string.isRequired,
      training: PropTypes.shape({
        category_id: PropTypes.number.isRequired,
        last_train: PropTypes.string,
      }),
    }).isRequired
  ).isRequired,
  categories: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number.isRequired,
      label: PropTypes.string.isRequired,
    }).isRequired
  ).isRequired,
  generatedText: PropTypes.string,
}

export default connect(mapStateToProps, mapDispatchToProps)(TextGenerator)
