import React from 'react'
import PropTypes from 'prop-types'

const TextGenerator = ({ algorithmes, categories}) => (
  <div>
    <form>
      Algorithmes displonibles : <select name="algo">
        {algorithmes.map(algorithm => (
          <option key={algorithm.id} value={algorithm.label}>
            {algorithm.label}
          </option>
        ))}
     </select>
     Catégories : <select name="cat">
       {categories.map(category => (
         <option key={category.id} value={category.label}>
           {category.label}
         </option>
       ))}
    </select>
    <button>Génère un texte !!</button>
    <textarea name="message" rows="10" cols="30">
    </textarea>
   </form>
  </div>
)

TextGenerator.propTypes = {
  algorithmes: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number.isRequired,
      label: PropTypes.string.isRequired,
    }).isRequired
  ).isRequired,
  categories: PropTypes.arrayOf(
    PropTypes.shape({
      id: PropTypes.number.isRequired,
      label: PropTypes.string.isRequired,
    }).isRequired
  ).isRequired,
}

export default TextGenerator
