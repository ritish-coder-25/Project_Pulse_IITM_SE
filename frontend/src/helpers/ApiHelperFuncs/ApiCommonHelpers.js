export class ApiCommonHelpers {
  static getAxiosError(error) {
    if (error.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      console.log(error.response.data)
      //console.log(error.response.status)
      //console.log(error.response.headers)
      return {
        isResponseError: true,
        error: JSON.parse(error.response.data),
        status: error.response.status,
      }
    } else {
      // Something happened in setting up the request that triggered an Error
      console.log('Error', error.message)
      return { isResponseError: false, errorMessage: error.message }
    }
  }
}
