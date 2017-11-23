import React from 'react'
import PropTypes from 'prop-types'

const Category = ({ label }) => <li>{label}</li>

Category.propTypes = {
  label: PropTypes.string.isRequired,
}

export default Category
