import React from 'react'
import PropTypes from 'prop-types'
import { bindActionCreators } from 'redux'
import { connect } from 'react-redux'

import { login, logout, register, githubLogin } from '../actions'

class NavBar extends React.Component {
  constructor(props, context) {
    super(props, context)
    this.state = {
      currentAction: 'init',
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
    if (nextProps.user !== null) {
      this.setState({ currentAction: 'isLogged' })
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

  displayForm(event, actionType) {
    event.preventDefault()
    this.setState({
      currentAction: actionType,
      formData: {
        username: '',
        email: '',
        password: '',
      },
    })
  }

  submitForm() {
    switch (this.state.currentAction) {
      case 'login':
        this.props.actions.login(
          this.state.formData.email,
          this.state.formData.password
        )
        break
      case 'register':
        this.props.actions.register(
          this.state.formData.username,
          this.state.formData.email,
          this.state.formData.password
        )
        break
      default:
        this.setState({ currentAction: 'init' })
    }
  }

  cancelFormOrLogout() {
    this.props.actions.logout()
    this.setState({ currentAction: 'init' })
  }

  githubLogin() {
    this.props.actions.githubLogin()
  }

  render() {
    return (
      <div>
        <h1>PyRaTe</h1>

        {this.state.currentAction === 'init' && (
          <div>
            <button onClick={event => this.displayForm(event, 'login')}>
              Login
            </button>
            <button onClick={event => this.displayForm(event, 'register')}>
              Register
            </button>{' '}
            <button onClick={event => this.githubLogin(event, 'register')}>
              Log with GitHub
            </button>
          </div>
        )}
        {(this.state.currentAction === 'login' ||
          this.state.currentAction === 'register') && (
          <div>
            <form onSubmit={event => this.formPreventDefault(event)}>
              {this.state.currentAction === 'register' && (
                <input
                  name="username"
                  placeholder="username"
                  required
                  onChange={event => this.handleFormChange(event)}
                />
              )}
              <input
                name="email"
                type="email"
                placeholder="email"
                required
                onChange={event => this.handleFormChange(event)}
              />
              <input
                name="password"
                type="password"
                placeholder="password"
                required
                onChange={event => this.handleFormChange(event)}
              />
              <button onClick={event => this.submitForm(event)}>Submit</button>
              <button onClick={() => this.cancelFormOrLogout()}>Cancel</button>
            </form>
          </div>
        )}
        {this.state.currentAction === 'isLogged' && (
          <div>
            Hello {this.state.user.username} !
            <button onClick={() => this.cancelFormOrLogout()}>Logout</button>
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
    actions: bindActionCreators(
      { login, logout, register, githubLogin },
      dispatch
    ),
  }
}

NavBar.propTypes = {
  actions: PropTypes.object.isRequired,
  message: PropTypes.string.isRequired,
  user: PropTypes.shape({
    id: PropTypes.number.isRequired,
    username: PropTypes.string.isRequired,
    email: PropTypes.string,
    isAdmin: PropTypes.bool.isRequired,
    createdAt: PropTypes.string.isRequired,
  }),
}

export default connect(mapStateToProps, mapDispatchToProps)(NavBar)
