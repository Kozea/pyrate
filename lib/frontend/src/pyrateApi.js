const apiUrl = 'http://localhost:18201/api/'

class PyrateApi {
  static getAllAlgorithmes() {
    return fetch(`${apiUrl}algorithmes`).then(response => response.json())
    .catch(error => error)
  }
  static getAllCategories() {
    return fetch(`${apiUrl}categories`).then(response => response.json())
    .catch(error => error)
  }
  static train(algo, categoryId) {
    const request = new Request(`${apiUrl}train`, {
      method: 'POST',
      headers: new Headers({
        'Content-Type': 'application/json'
      }),
      body: JSON.stringify({
        algo: algo,
        category_id: categoryId
      })
    })
    return fetch(request).then(response => response.json())
    .catch(error => error)
  }
  static generateText(algo, categoryId) {
    const request = new Request(`${apiUrl}generate`, {
      method: 'POST',
      headers: new Headers({
        'Content-Type': 'application/json'
      }),
      body: JSON.stringify({
        algo: algo,
        category_id: categoryId
      })
    })
    return fetch(request).then(response => response.json())
    .catch(error => error)
  }
}

export default PyrateApi
