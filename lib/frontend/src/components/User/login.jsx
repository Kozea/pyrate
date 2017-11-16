import React from 'react'

export default function Login() {
  return (
    <div>
      <label>
        Email: <input id="email" type="text" />{' '}
      </label>
      <br />
      <label>
        Password: <input id="input1" type="password" />
      </label>
      <div>
        <button type="button" onClick={() => (window.location.href = '/')}>
          Cancel
        </button>
        <button type="submit">Sign Up</button>
      </div>
    </div>
  )
}
