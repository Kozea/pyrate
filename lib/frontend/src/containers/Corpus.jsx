import React from 'react'
import PropTypes from 'prop-types'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'

import { loadCorpusTexts, addCorpusTexts, deleteCorpusTexts } from '../actions'

class Corpus extends React.Component {
  constructor(props, context) {
    super(props, context)
    this.state = {
      categories: this.props.categories,
      corpusTexts: this.props.corpusTexts,
      message: this.props.message,
      selectedCategory: {
        id: null,
        owner_id: null,
      },
      user: this.props.user,
    }
  }

  componentWillReceiveProps(nextProps) {
    const selectedCategory = nextProps.categories[0]
      ? {
          id: nextProps.categories[0].id,
          owner_id: nextProps.categories[0].owner_id,
        }
      : { id: null, owner_id: null }

    if (this.props.categories !== nextProps.categories) {
      this.setState({
        categories: nextProps.categories,
        selectedCategory: {
          id: selectedCategory.id,
          owner_id: selectedCategory.owner_id,
        },
      })
      this.props.actions.loadCorpusTexts(selectedCategory.id)
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
    const catIdOwnedId = event.target.value.split('|')
    const selectedCategory = {
      id: parseInt(catIdOwnedId[0]),
      owner_id: parseInt(catIdOwnedId[1]),
    }
    this.setState({ selectedCategory: selectedCategory })
    this.props.actions.loadCorpusTexts(catIdOwnedId[0])
  }

  uploadFile(event) {
    event.preventDefault()
    const form = new FormData()
    form.append('file', event.target.textFile.files[0])
    form.append(
      'data',
      `{"title": "${event.target.title.value}", "category_id": ${
        this.state.selectedCategory.id
      }}`
    )
    this.props.actions.addCorpusTexts(form, this.state.selectedCategory.id)
  }

  deleteFile(textId) {
    this.props.actions.deleteCorpusTexts(textId, this.state.selectedCategory.id)
  }

  render() {
    return (
      <div>
        Liste des textes selon la catégorie du corpus :
        <select name="cat" onChange={event => this.handleCatChange(event)}>
          {this.state.categories.map(category => (
            <option
              key={category.id}
              value={`${category.id}|${category.owner_id}`}
            >
              {category.label} ({category.owner_username})
            </option>
          ))}
        </select>
        <ul>
          {this.state.corpusTexts.map(text => (
            <li key={text.id}>
              {text.title} (ajouté le {text.creation_date}, par{' '}
              {text.owner_username})
              {this.state.user &&
                (this.state.user.id === text.owner_id ||
                  this.state.user.isAdmin) && (
                  <div>
                    <button
                      type="submit"
                      onClick={() => this.deleteFile(text.id)}
                    >
                      Supprimer
                    </button>
                  </div>
                )}
            </li>
          ))}
        </ul>
        {this.state.user &&
          (this.state.selectedCategory.owner_id === this.state.user.id ||
            this.state.user.isAdmin) && (
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
    actions: bindActionCreators(
      { loadCorpusTexts, addCorpusTexts, deleteCorpusTexts },
      dispatch
    ),
  }
}

Corpus.propTypes = {
  categories: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number.isRequired,
      label: PropTypes.string.isRequired,
      owner_id: PropTypes.number.isRequired,
    }).isRequired
  ).isRequired,
  corpusTexts: PropTypes.arrayOf(
    PropTypes.shape({
      creation_date: PropTypes.string.isRequired,
      id: PropTypes.number.isRequired,
      title: PropTypes.string.isRequired,
      owner_id: PropTypes.number.isRequired,
      owner_username: PropTypes.string.isRequired,
    })
  ).isRequired,
  message: PropTypes.string.isRequired,
  user: PropTypes.shape({
    id: PropTypes.number.isRequired,
    username: PropTypes.string.isRequired,
    email: PropTypes.string.isRequired,
    isAdmin: PropTypes.bool.isRequired,
    createdAt: PropTypes.string.isRequired,
  }),
}

export default connect(mapStateToProps, mapDispatchToProps)(Corpus)
