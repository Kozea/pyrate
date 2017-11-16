import React from 'react'

export default function Login() {
  return (
    <div>
      <label>
        Email: <input id="email" type="text" placeholder="email" />{' '}
      </label>
      <br />
      <label>
        Mot de passe:{' '}
        <input id="input1" type="password" placeholder="password" />
      </label>
      <div>
        <button type="button" onClick={() => (window.location.href = '/')}>
          Annuler
        </button>
        <button type="submit">Valider</button>
      </div>
    </div>
  )
}
