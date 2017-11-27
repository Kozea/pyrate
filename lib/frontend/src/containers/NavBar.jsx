import React from 'react'
import PropTypes from 'prop-types'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'

import { login, logout, register } from '../actions'

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
      authMessage: '',
      user: this.props.user,
    }
  }

  componentWillReceiveProps(nextProps) {
    if (this.props.isAuthenticated !== nextProps.isAuthenticated) {
      this.setState({ isAuthenticated: nextProps.isAuthenticated })
    }
    if (this.props.authMessage !== nextProps.authMessage) {
      this.setState({ authMessage: nextProps.authMessage })
    }
    if (this.props.user !== nextProps.user) {
      this.setState({ user: nextProps.user })
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

  register(event) {
    event.preventDefault()
    this.props.actions.register(
      this.state.formData.username,
      this.state.formData.email,
      this.state.formData.password
    )
  }

  logout(event) {
    event.preventDefault()
    this.props.actions.logout()
  }

  render() {
    return (
      <div>
        <h1>PyRaTe</h1>
        {!this.state.isAuthenticated &&
          <div>
            <form onSubmit={event => this.formPreventDefault(event)} >
              <input
               name="username"
               onChange={event => this.handleFormChange(event)}
              />
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
              <button
               onClick={event => this.register(event)}
              >
                Register
              </button>
            </form>
          </div>
        }
        {this.state.isAuthenticated &&
          <div>
            Hello !
            <button
              onClick={event => this.logout(event)}
            >
              Logout
            </button>
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
    user: state.user
  }
}
function mapDispatchToProps(dispatch) {
  return {
    actions: bindActionCreators({ login, logout, register }, dispatch)
  }
}

NavBar.propTypes = {
  actions: PropTypes.object.isRequired,
  isAuthenticated: PropTypes.bool.isRequired,
  user: PropTypes.shape({
      username: PropTypes.string.isRequired,
      email: PropTypes.string.isRequired,
      isAdmin: PropTypes.bool.isRequired,
      createdAt: PropTypes.string.isRequired,
  })
}

export default connect(mapStateToProps, mapDispatchToProps)(NavBar)
