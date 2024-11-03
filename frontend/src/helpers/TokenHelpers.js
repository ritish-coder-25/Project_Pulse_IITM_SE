export const isJwtTokenExpired = token => {
  if (!token) {
    return false
  }
  var tokenParts = token.split('.')
  var base64Url = tokenParts[1]
  var base64 = base64Url.replace(/-/g, '+').replace(/_/g, '/')
  console.log('got base64')
  var decodedToken = JSON.parse(atob(base64))
  if (Date.now() / 1000 >= decodedToken.exp) {
    return true
  }
  return false
}
