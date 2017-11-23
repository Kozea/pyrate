import React from 'react'
import PropTypes from 'prop-types'

const AlgorithmesList = ({ algorithmes }) => (
  <div>
    <form>
      Algorithm: <select name="algo">
        {algorithmes.map(algorithm => (
          <option key={algorithm.id} value={algorithm.label}>
            {algorithm.label}
          </option>
        ))}
     </select>
   </form>
  </div>
)

AlgorithmesList.propTypes = {
  algorithmes: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number.isRequired,
      label: PropTypes.string.isRequired,
    }).isRequired
  ).isRequired,
}

export default AlgorithmesList
