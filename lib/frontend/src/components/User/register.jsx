import React from 'react'

export default function Register() {
  return (
    <div>
      <label>Nom d&apos;utilisateur : </label>
      <input type="text" placeholder="username" name="username" required />
      <br />

      <label>Email : </label>
      <input type="text" placeholder="email" name="email" required />
      <br />

      <label>Mot de passe : </label>
      <input type="password" placeholder="password" name="psw" required />
      <br />

      <label>Confirmation du mot de passe : </label>
      <input
        type="password"
        placeholder="password"
        name="psw-repeat"
        required
      />
      <br />

      <p>
        La création d&apos;un compte implique que vous avez lu et accepté les{' '}
        <a href="#">termes et conditions d&apos;utilisation</a>.
      </p>
      <br />

      <div>
        <button type="button" onClick={() => (window.location.href = '/')}>
          Annuler
        </button>
        <button type="submit">Valider</button>
      </div>
    </div>
  )
}
