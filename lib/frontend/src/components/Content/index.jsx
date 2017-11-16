import React from 'react'

class Content extends React.Component {
  constructor() {
    super()
    this.state = {
      showReply: false,
    }
  }

  render() {
    return (
      <div className="content">
        <label>Category : </label>
        <select>
          <option>Stage</option>
          <option>Reports</option>
        </select>
        <br />
        <button>Generate</button>
        <br />
        <label>Result : </label>
        <br />
        <output />
        <button>Save</button>
      </div>
    )
  }
}

export default Content
