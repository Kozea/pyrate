import React from 'react'

class Corpus extends React.Component {
  constructor() {
    super()
    this.state = {
      showReply: false,
    }
  }

  render() {
    return (
      <div>
        <label>Corpus : </label>
        <ul>
          <li>
            <span className="corpustitle">Les Misérables, de Victor HUGO</span>
            <button>Edit</button> <button>Delete</button>
          </li>
          <li>
            <span className="corpustitle">etcc</span>
            <button>Edit</button> <button>Delete</button>
          </li>
          <li>
            <span className="corpustitle">etcccc</span>
            <button>Edit</button> <button>Delete</button>
          </li>
        </ul>
        <button>Add a corpus</button>
      </div>
    )
  }
}

export default Corpus
