import React from 'react'
import PropTypes from 'prop-types'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'

import { login, logout, register } from '../actions'

class NavBar extends React.Component {
  constructor(props, context) {
    super(props, context)
    this.state = {
      formData: {
        username: '',
        email: '',
        password: '',
      },
      message: this.props.message,
      user: this.props.user,
    }
  }

  componentWillReceiveProps(nextProps) {
    if (this.props.user !== nextProps.user) {
      this.setState({ user: nextProps.user })
    }
    if (this.props.message !== nextProps.message) {
      this.setState({ message: nextProps.message })
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
        {!this.state.user && (
          <div>
            <form onSubmit={event => this.formPreventDefault(event)}>
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
              <button onClick={event => this.login(event)}>Login</button>
              <button onClick={event => this.register(event)}>Register</button>
            </form>
          </div>
        )}
        {this.state.user && (
          <div>
            Hello {this.state.user.username} !
            <button onClick={event => this.logout(event)}>Logout</button>
          </div>
        )}
        {this.state.message}
      </div>
    )
  }
}

function mapStateToProps(state) {
  return {
    user: state.user,
    message: state.message,
  }
}
function mapDispatchToProps(dispatch) {
  return {
    actions: bindActionCreators({ login, logout, register }, dispatch),
  }
}

NavBar.propTypes = {
  actions: PropTypes.object.isRequired,
  message: PropTypes.string.isRequired,
  user: PropTypes.shape({
    username: PropTypes.string.isRequired,
    email: PropTypes.string.isRequired,
    isAdmin: PropTypes.bool.isRequired,
    createdAt: PropTypes.string.isRequired,
  }),
}

export default connect(mapStateToProps, mapDispatchToProps)(NavBar)
