const apiUrl = "http://localhost:18201/api/"

class PyrateApi {
  static getAllCategories() {
    return fetch(apiUrl + 'categories').then(response => {
      return response.json();
    }).catch(error => {
      return error;
    });
  }
}

export default PyrateApi;