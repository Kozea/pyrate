const apiUrl = "http://localhost:18201/api/"

class PyrateApi {
  static getAllAlgorithmes() {
    return fetch(`${apiUrl}algorithmes`).then(response => {
      return response.json();
    }).catch(error => {
      return error;
    });
  }
  static getAllCategories() {
    return fetch(`${apiUrl}categories`).then(response => {
      return response.json();
    }).catch(error => {
      return error;
    });
  }
  static train(algo, category_id){
    const request = new Request(`${apiUrl}train`, {
      method: 'POST',
      headers: new Headers({
        'Content-Type': 'application/json'
      }),
      body: JSON.stringify({
        algo: algo,
        category_id: category_id
      })
    })
    return fetch(request).then(response => {
      return response.json();
    }).catch(error => {
      return error;
    });
  }
  static generateText(algo, category_id){
    const request = new Request(`${apiUrl}generate`, {
      method: 'POST',
      headers: new Headers({
        'Content-Type': 'application/json'
      }),
      body: JSON.stringify({
        algo: algo,
        category_id: category_id
      })
    })
    return fetch(request).then(response => {
      return response.json();
    }).catch(error => {
      return error;
    });
  }
}

export default PyrateApi;
