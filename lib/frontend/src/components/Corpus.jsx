import React from 'react'
import PropTypes from 'prop-types'

const Corpus = ({ title }) => <li>{title}</li>

Corpus.propTypes = {
  title: PropTypes.string.isRequired,
}

export default Corpus
