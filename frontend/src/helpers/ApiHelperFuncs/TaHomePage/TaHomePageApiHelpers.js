import { mainAxios } from '@/helpers/ApiHelpers'
import TaHomePageApiHelpersJson from './TaHomePageApiHelpers.json' assert { type: 'json' }
import { UserRoleEnums } from '@/enums'

export class TaHomePageApiHelpers {
  static async fetchPendusers() {
    try {
      const response = await mainAxios.get('/users/pendusers')
      return response.data
    } catch (error) {
      console.warn('Using local pending user data due to error:', error)
      // TODO: REMOVE local data
      return TaHomePageApiHelpersJson.localPendusers
    }
  }

  static async fetchUploads() {
    try {
      const response = await mainAxios.get('/submissions/uploads')
      return response.data
    } catch (error) {
      console.warn('Using local uploads data due to error:', error)
      // TODO: REMOVE local data
      return TaHomePageApiHelpersJson.localUploads
    }
  }

  static async fetchCommits() {
    try {
      const response = await mainAxios.get('/commits')
      return response.data
    } catch (error) {
      console.warn('Using local commit data due to error:', error)
      // TODO: REMOVE local data
      return TaHomePageApiHelpersJson.localCommits
    }
  }

  static async fetchMilecomps() {
    try {
      const response = await mainAxios.get('/project/milecomps')
      return response.data
    } catch (error) {
      console.warn('Using local milestone completion data due to error:', error)
      // TODO: REMOVE local data
      return TaHomePageApiHelpersJson.localMilecomps
    }
  }

  static async approveuser(userData) {
    try {
      const response = await mainAxios.post('/users/approve_users', JSON.stringify(userData),
        { "headers": { "Content-Type": "application/json", "Authorization": "Bearer " + localStorage.getItem("access_token") } });

      return response.data
    } catch (error) {
      console.warn("Error approving user:", error.message)
      if (error.response) {
        console.warn('Error response:', error.response.data)
      } else if (error.request) {
        console.warn('No response received:', error.request)
      }
      throw error
    }
  }
}
