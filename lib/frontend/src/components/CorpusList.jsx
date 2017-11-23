import React from 'react'
import PropTypes from 'prop-types'

const CorpusList = ({ corpus }) => (
  <div>
    {/* {console.log(corpus)} */}
    <ul>
      Listes des Corpus ...{corpus.map(uncorpus => (
        <li key={uncorpus.id}>
          {uncorpus.title}
          {/* VOIR COMMENT METTRE filename, date, etc */}
          <button>Supprimer</button>
        </li>
      ))}
    </ul>
  </div>
)

CorpusList.propTypes = {
  corpus: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number.isRequired,
      title: PropTypes.string.isRequired,
    }).isRequired
  ).isRequired,
}

export default CorpusList
