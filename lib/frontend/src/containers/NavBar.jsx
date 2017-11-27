import React from 'react'
import PropTypes from 'prop-types'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'

import { login, } from '../actions'

class NavBar extends React.Component {

  constructor (props, context) {
    super(props, context)
    this.state = {
      isAuthenticated: this.props.isAuthenticated,
      formData: {
        username: '',
        email: '',
        password: ''
      },
      authMessage: ''
    }
  }

  componentWillReceiveProps(nextProps) {
    if (this.props.isAuthenticated !== nextProps.isAuthenticated) {
      this.setState({ isAuthenticated: nextProps.isAuthenticated })
    }
    if (this.props.authMessage !== nextProps.authMessage) {
      this.setState({ authMessage: nextProps.authMessage })
    }
  }

  formPreventDefault(event) {
    event.preventDefault()
  }

  handleFormChange(event) {
    const { formData } = this.state
    formData[event.target.name] = event.target.value
    this.forceUpdate()
  }

  login(event) {
    event.preventDefault()
    this.props.actions.login(
      this.state.formData.email,
      this.state.formData.password
    )
  }

  render() {
    return (
      <div>
        <h1>PyRaTe</h1>
        {!this.state.isAuthenticated &&
          <div>
            <form onSubmit={event => this.formPreventDefault(event)} >
              <input
               name="email"
               required
               onChange={event => this.handleFormChange(event)}
              />
              <input
               name="password"
               type="password"
               required
               onChange={event => this.handleFormChange(event)}
              />
              <button
               onClick={event => this.login(event)}
              >
                Login
              </button>
            </form>
          </div>
        }
        {this.state.isAuthenticated &&
          <div>
            <form onSubmit={event => this.formPreventDefault(event)} >
              <button>
                Logout
              </button>
            </form>
          </div>
        }
        {this.state.authMessage}
      </div>
    )
  }

}

function mapStateToProps(state) {
  return {
    isAuthenticated: state.isAuthenticated,
  }
}
function mapDispatchToProps(dispatch) {
  return {
    actions: bindActionCreators({ login, }, dispatch)
  }
}

NavBar.propTypes = {
  actions: PropTypes.object.isRequired,
  isAuthenticated: PropTypes.bool.isRequired,
}

export default connect(mapStateToProps, mapDispatchToProps)(NavBar)
