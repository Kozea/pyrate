import React from 'react'
import PropTypes from 'prop-types'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'

import { loadCorpusTexts } from '../actions'

class Corpus extends React.Component {
  constructor(props, context) {
    super(props, context)
    this.state = {
      categories: this.props.categories,
      corpusTexts: this.props.corpusTexts,
      message: this.props.message,
      selectedCategory: '',
    }
  }

  componentWillReceiveProps(nextProps) {
    const selectedCategory = nextProps.categories[0]
      ? nextProps.categories[0].id
      : ''

    if (this.props.categories !== nextProps.categories) {
      this.setState({
        categories: nextProps.categories,
        selectedCategory: selectedCategory,
      })
      this.props.actions.loadCorpusTexts(selectedCategory)
    }
    if (this.props.corpusTexts !== nextProps.corpusTexts) {
      this.setState({ corpusTexts: nextProps.corpusTexts })
    }
    if (this.props.message !== nextProps.message) {
      this.setState({ message: nextProps.message })
    }
  }

  formPreventDefault(event) {
    event.preventDefault()
  }

  handleCatChange(event) {
    this.setState({ selectedCategory: event.target.value })
    this.props.actions.loadCorpusTexts(event.target.value)
  }

  render() {
    return (
      <div>
        Liste des textes selon la catégorie du corpus :
        <select name="cat" onChange={event => this.handleCatChange(event)}>
          {this.state.categories.map(category => (
            <option key={category.id} value={category.id}>
              {category.label}
            </option>
          ))}
        </select>
        <ul>
          {this.state.corpusTexts.map(text => (
            <li key={text.id}>
              {text.title} (ajouté le {text.creation_date})
            </li>
          ))}
        </ul>
        <br />
        Ajouter un text au corpus :
        <form onSubmit={event => this.formPreventDefault(event)}>
          <input type="file" name="textFile" />
          <button>Envoyer</button>
        </form>
      </div>
    )
  }
}

function mapStateToProps(state) {
  return {
    categories: state.categories,
    corpusTexts: state.corpusTexts,
    message: state.message,
  }
}

function mapDispatchToProps(dispatch) {
  return {
    actions: bindActionCreators({ loadCorpusTexts }, dispatch),
  }
}

Corpus.propTypes = {
  categories: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number.isRequired,
      label: PropTypes.string.isRequired,
    }).isRequired
  ).isRequired,
  corpusTexts: PropTypes.arrayOf(
    PropTypes.shape({
      creation_date: PropTypes.string.isRequired,
      id: PropTypes.number.isRequired,
      title: PropTypes.string.isRequired,
      owner: PropTypes.number.isRequired,
    })
  ).isRequired,
  message: PropTypes.string.isRequired,
}

export default connect(mapStateToProps, mapDispatchToProps)(Corpus)
