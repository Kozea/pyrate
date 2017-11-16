import React from 'react'

export default function Register() {
  return (
    <div>
      <label>Username : </label>
      <input
        type="text"
        placeholder="Enter Username"
        name="username"
        required
      />
      <br />

      <label>Email : </label>
      <input type="text" placeholder="Enter Email" name="email" required />
      <br />

      <label>Password : </label>
      <input type="password" placeholder="Enter Password" name="psw" required />
      <br />

      <label>Repeat Password : </label>
      <input
        type="password"
        placeholder="Repeat Password"
        name="psw-repeat"
        required
      />
      <br />

      <p>
        By creating an account you agree to our <a href="#">Terms & Privacy</a>.
      </p>
      <br />

      <div>
        <button type="button" onClick={() => (window.location.href = '/')}>
          Cancel
        </button>
        <button type="submit">Sign Up</button>
      </div>
    </div>
  )
}
