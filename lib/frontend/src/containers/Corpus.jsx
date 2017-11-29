import React from 'react'
import PropTypes from 'prop-types'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'

import { loadCorpusTexts, addCorpusTexts } from '../actions'

class Corpus extends React.Component {
  constructor(props, context) {
    super(props, context)
    this.state = {
      categories: this.props.categories,
      corpusTexts: this.props.corpusTexts,
      message: this.props.message,
      selectedCategory: '',
      user: this.props.user,
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
    if (this.props.user !== nextProps.user) {
      this.setState({ user: nextProps.user })
    }
  }

  handleCatChange(event) {
    this.setState({ selectedCategory: event.target.value })
    this.props.actions.loadCorpusTexts(event.target.value)
  }

  uploadFile(event) {
    event.preventDefault()
    const form = new FormData()
    form.append('file', event.target.textFile.files[0])
    form.append(
      'data',
      `{"title": "${event.target.title.value}", "category_id": ${
        this.state.selectedCategory
      }}`
    )
    this.props.actions.addCorpusTexts(form, this.state.selectedCategory)
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
        {this.state.user && (
          <div>
            <br />
            Ajouter un texte au corpus :
            <form
              encType="multipart/form-data"
              onSubmit={event => this.uploadFile(event)}
            >
              <input name="title" placeholder="titre" required />
              <input type="file" name="textFile" accept=".txt" required />
              <br />
              <button type="submit">Envoyer</button>
            </form>
          </div>
        )}
      </div>
    )
  }
}

function mapStateToProps(state) {
  return {
    categories: state.categories,
    corpusTexts: state.corpusTexts,
    message: state.message,
    user: state.user,
  }
}

function mapDispatchToProps(dispatch) {
  return {
    actions: bindActionCreators({ loadCorpusTexts, addCorpusTexts }, dispatch),
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
  user: PropTypes.shape({
    username: PropTypes.string.isRequired,
    email: PropTypes.string.isRequired,
    isAdmin: PropTypes.bool.isRequired,
    createdAt: PropTypes.string.isRequired,
  }),
}

export default connect(mapStateToProps, mapDispatchToProps)(Corpus)
