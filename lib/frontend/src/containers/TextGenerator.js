import React from 'react'
import PropTypes from 'prop-types'

import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'

import * as allActions  from '../actions'

class TextGenerator extends React.Component {

  constructor (props, context) {
    super(props, context);
    this.state = {
      algorithmes: this.props.algorithmes,
      categories: this.props.categories,
      text: this.props.generatedText,
      selectedAlgo: "",
      selectedCategory: ""
    };
  }

  componentWillReceiveProps(nextProps) {
    if (this.props.algorithmes != nextProps.algorithmes) {
      this.setState({algorithmes: nextProps.algorithmes});
    }
    if (this.props.categories != nextProps.categories) {
      this.setState({categories: nextProps.categories});
    }
    if (this.props.text != nextProps.text) {
      this.setState({text: nextProps.text});
    }
  }

  // TODO: refactor
  handleAlgoChange(event){
    this.setState({selectedAlgo:event.target.value, text: ""});
  }
  handleCatChange(event){
    this.setState({selectedCategory:event.target.value, text: ""});
  }

  runGenText(event) {
    event.preventDefault();
    this.props.actions.generateText(
      this.state.selectedAlgo,
      parseInt(this.state.selectedCategory))
  }

  render(){
    return (
      <div>
        <form onSubmit={(event) => this.runGenText(event)} >
          Algorithmes displonibles :
          <select
           name="algo"
           onChange={(event) => this.handleAlgoChange(event)}
           >
            {this.state.algorithmes.map(algorithm => (
              <option key={algorithm.id} value={algorithm.label}>
                {algorithm.label}
              </option>
            ))}
           </select>
           Catégories :
           <select
            name="cat"
            onChange={(event) => this.handleCatChange(event)}
            >
             {this.state.categories.map(category => (
               <option key={category.id} value={category.id}>
                 {category.label}
               </option>
             ))}
           </select>
           <button>Génère un texte !!</button>
           <textarea name="message" rows="10" cols="30" value={this.state.text}>
           </textarea>
         </form>
        </div>
    )
  }
}

function mapStateToProps(state, ownProps) {
  return {
    algorithmes: state.algorithmes,
    categories: state.categories,
    text: state.generatedText,
  }
}
function mapDispatchToProps(dispatch) {
  return {
    actions: bindActionCreators(allActions, dispatch)
  }
}

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
  generatedText: PropTypes.string,
  actions: PropTypes.object.isRequired
}


export default connect(mapStateToProps, mapDispatchToProps)(TextGenerator);
