import React from 'react'

class Categories extends React.Component {
  constructor() {
    super()
    this.state = {
      showReply: false,
    }
  }

  render() {
    return (
      <div>
        <label>Categories : </label>
        <ul>
          <li>
            Novels <button>Edit</button> <button>Delete</button>
          </li>
          <li>
            Newspapers <button>Edit</button> <button>Delete</button>
          </li>
          <li>
            Reports <button>Edit</button> <button>Delete</button>
          </li>
        </ul>
        <button>Add a category</button>
      </div>
    )
  }
}

export default Categories
