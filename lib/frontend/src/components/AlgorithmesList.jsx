import React from 'react'
import PropTypes from 'prop-types'

// TODO: handle trainings to dipslay on which corpus algo is trained
const AlgorithmesList = ({ algorithmes }) => (
  <div> {console.log(algorithmes)}
    Liste des Algorithmes disponibles :
    <ul>
      {algorithmes.map(algorithm => (
        <li key={algorithm.id}>
          {algorithm.label}
        </li>
      ))}
    </ul>
  </div>
)

// TODO: training propTypes
AlgorithmesList.propTypes = {
  algorithmes: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number.isRequired,
      label: PropTypes.string.isRequired,
    }).isRequired
  ).isRequired,
}

export default AlgorithmesList
