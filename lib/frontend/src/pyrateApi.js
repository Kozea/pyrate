const apiUrl = 'http://localhost:18201/api/'

class PyrateApi {
  static login(email, password) {
    const request = new Request(`${apiUrl}auth/login`, {
      method: 'POST',
      headers: new Headers({
        'Content-Type': 'application/json',
      }),
      body: JSON.stringify({
        email: email,
        password: password,
      }),
    })
    return fetch(request)
      .then(response => response.json())
      .catch(error => error)
  }
  static register(username, email, password) {
    const request = new Request(`${apiUrl}auth/register`, {
      method: 'POST',
      headers: new Headers({
        'Content-Type': 'application/json',
      }),
      body: JSON.stringify({
        username: username,
        email: email,
        password: password,
      }),
    })
    return fetch(request)
      .then(response => response.json())
      .catch(error => error)
  }
  static getAllAlgorithmes() {
    return fetch(`${apiUrl}algorithmes`)
      .then(response => response.json())
      .catch(error => error)
  }
  static getAllCategories() {
    return fetch(`${apiUrl}categories`)
      .then(response => response.json())
      .catch(error => error)
  }
  static train(algo, categoryId) {
    const request = new Request(`${apiUrl}train`, {
      method: 'POST',
      headers: new Headers({
        'Content-Type': 'application/json',
      }),
      body: JSON.stringify({
        algo: algo,
        category_id: categoryId,
      }),
    })
    return fetch(request)
      .then(response => response.json())
      .catch(error => error)
  }
  static generateText(algo, categoryId) {
    const request = new Request(`${apiUrl}generate`, {
      method: 'POST',
      headers: new Headers({
        'Content-Type': 'application/json',
      }),
      body: JSON.stringify({
        algo: algo,
        category_id: categoryId,
      }),
    })
    return fetch(request)
      .then(response => response.json())
      .catch(error => error)
  }
  static deleteCategory(categoryId) {
    const request = new Request(`${apiUrl}categories/${categoryId}`, {
      method: 'DELETE',
      headers: new Headers({
        'Content-Type': 'application/json',
        Authorization: `Bearer ${window.localStorage.getItem('authToken')}`,
      }),
    })
    return fetch(request)
      .then(response => response.json())
      .catch(error => error)
  }
  static addCategory(label) {
    const request = new Request(`${apiUrl}categories`, {
      method: 'POST',
      headers: new Headers({
        'Content-Type': 'application/json',
        Authorization: `Bearer ${window.localStorage.getItem('authToken')}`,
      }),
      body: JSON.stringify({
        label: label,
      }),
    })
    return fetch(request)
      .then(response => response.json())
      .catch(error => error)
  }

  static updateCat(categoryId, catLabel) {
    const request = new Request(`${apiUrl}categories/${categoryId}`, {
      method: 'PUT',
      headers: new Headers({
        'Content-Type': 'application/json',
        Authorization: `Bearer ${window.localStorage.getItem('authToken')}`,
      }),
      body: JSON.stringify({
        label: catLabel,
      }),
    })
    return fetch(request)
      .then(response => response.json())
      .catch(error => error)
  }
}

export default PyrateApi
