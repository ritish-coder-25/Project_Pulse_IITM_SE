import { Axios, HttpStatusCode } from 'axios'
import { LocalStorageEnums } from '../enums'

export const BASE_URL = 'http://localhost:5000/api'

const axios = new Axios({
  baseURL: BASE_URL,
  timeout: 5000,
  validateStatus: status => {
    if (status >= 200 && status < 400) {
      return true
    }
    return false
  },
  headers: {
    'Content-Type': 'application/json',
  }
})

axios.interceptors.request.use(
  value => {
    const token = localStorage.getItem(LocalStorageEnums.accessToken)
    if (token) {
      value.headers.Authorization = `Bearer ${token}`
    }
    value.headers['Content-Type'] = 'application/json'
    return value
  },
  error => {
    return Promise.reject(error)
  },
)

// // Add a response interceptor
// axios.interceptors.response.use(
//   function (response) {
//     // Any status code that lie within the range of 2xx cause this function to trigger
//     // Do something with response data
//     return response
//   },
//   function (error) {
//     // Any status codes that falls outside the range of 2xx cause this function to trigger
//     // Do something with response error
//     const originalRequest = error.config
//     const errorData = JSON.parse(error.response.data)
//     console.log("errorresponse",error.response.data, JSON.parse(error.response.data))
//     if (error.response.status === 401 && !originalRequest._retry && errorData.error_code !== "ROLE001") {
//       originalRequest._retry = true
//       return RefreshTokenAxios().then(() => {
//         originalRequest.headers.Authorization = `Bearer ${localStorage.getItem(
//           LocalStorageEnums.accessToken
//         )}`
//         return new Axios(originalRequest)
//       })
//     }
//     return Promise.reject(error)
//   }
// )

// export const RefreshTokenAxios = async () => {
//   try {
//     const axios = new Axios({
//       baseURL: BASE_URL,
//       timeout: 5000
//     })
//     const refresh = await axios.post('/refreshtoken', null, {
//       headers: {
//         Authorization: `Bearer ${localStorage.getItem(LocalStorageEnums.refreshToken)}`
//       }
//     })
//     console.log('refreshtoken status', refresh)
//     if (refresh.status === HttpStatusCode.Ok) {
//       console.log('saved the refresht tokens')
//       const tokens = JSON.parse(refresh.data)
//       localStorage.setItem(LocalStorageEnums.accessToken, tokens.access_token)
//       localStorage.setItem(LocalStorageEnums.refreshToken, tokens.refresh_token)
//     }
//     return true
//   } catch (err) {
//     return false
//   }
// }

export const mainAxios = axios
