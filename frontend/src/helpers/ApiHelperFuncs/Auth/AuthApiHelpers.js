import { mainAxios } from '@/helpers/ApiHelpers'
import { ApiCommonHelpers } from '../ApiCommonHelpers'

export class AuthApiHelper {
  static async signup(data) {
    try {
      const signupData = this.signupDataToDto(data)
      console.log('signupData: ', signupData)
      const sr = await mainAxios.post(
        '/auth/register',
        JSON.stringify(signupData),
      )
      return {
        isSuccess: true,
        message: sr.data.message,
      }
    } catch (err) {
      const { error, isResponseError } = ApiCommonHelpers.getAxiosError(err)
      return {
        isSuccess: false,
        error,
        isResponseError,
      }
      //console.log(error.config);
    }
  }

  static signupDataToDto(data) {
    const dto = {
      first_name: data.firstName,
      last_name: data.lastName,
      username: data.username,
      password: data.password,
      student_email: data.email,
      github_username: data.githubUsername,
      discord_username: data.discordUsername,
    }
    return dto
  }

  static async login(data) {
    try {
      const loginData = {
        student_email: data.student_email,
        password: data.password,
      }
      const stringifiedData = JSON.stringify(loginData)
      console.log("stringifiedData: ", stringifiedData)
      const sr = await mainAxios.post('/auth/login', stringifiedData)
      //console.log("sr: ", sr)
      const jsonSr = JSON.parse(sr.data)
      console.log("jsonsr", jsonSr);
      return {
        isSuccess: true,
        accessToken: jsonSr.access_token,
        user: jsonSr.user
      }
    } catch (err) {
      const { error, isResponseError, status, errorMessage } =
        ApiCommonHelpers.getAxiosError(err)
      return {
        isSuccess: false,
        error,
        isResponseError,
        errorMessage,
      }
      //console.log(error.config);
    }
  }
}
