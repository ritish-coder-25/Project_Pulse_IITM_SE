import { mainAxios } from '@/helpers/ApiHelpers'
import { ApiCommonHelpers } from '../ApiCommonHelpers'
import DefineTeamEmailsJson from './DefineTeamEmails.json' assert { type: 'json' }

export class DefineTeamApiHelper {
  static async defineTeam(data) {
    const response = await fetch('http://localhost:5000/defineTeam', {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    })
    return response.json()
  }

  static async fetchEmails() {
    //const response = await fetch('./DefineTeamEmails.json')
    //const data = await response.json()
    return DefineTeamEmailsJson.emails
  }

  static async fetchTeam() {
    try {
      const response = await fetch('/api/emails')
      if (!response.ok) {
        throw new Error('Failed to fetch emails')
      }
      const data = await response.json()
      return data.emails // Ensure your JSON has an "emails" array
    } catch (error) {
      console.error('Error fetching team:', error)
    }
  }

  static getEmailsFromMembers(members) {
    return Object.values(members).map(member => member.email)
  }

  static async getTeam() {
    try {
      const sr = await mainAxios.get('/teams')
      //console.log('sr: ', sr.data)
      const jsonSr = JSON.parse(sr.data).team
      //console.log('jsonsr', jsonSr)
      const emails = this.getEmailsFromMembers(jsonSr.members)
      return {
        isSuccess: true,
        github_repo_url: jsonSr.github_repo_url,
        teamId: jsonSr.id,
        members: jsonSr.members,
        team: jsonSr.name,
        projectId: jsonSr.project_id,
        teamLeadId: jsonSr.team_lead_id,
        mileStoneStatuses: jsonSr.milestone_statuses,
        emails,
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

  static async updateTeam(data) {
    try {
      const apiData = {
        team_id: data.team_id,
        emails: data.emails,
      }
      const stringifiedData = JSON.stringify(apiData)
      //console.log('stringifiedData: ', stringifiedData)
      const sr = await mainAxios.put(`/teams/${data.team_id}`, stringifiedData)
      //console.log("sr: ", sr)
      const jsonSr = JSON.parse(sr.data)
      console.log('jsonsr', jsonSr)
      return {
        isSuccess: true,
        message: jsonSr.message,
        team: jsonSr.team,
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

  static async createTeam(data) {
    try {
      const apiData = {
        team: data.team,
        github_repo_url: data.github_repo_url,
        emails: data.emails,
      }
      const stringifiedData = JSON.stringify(apiData)
      //console.log('stringifiedData: ', stringifiedData)
      const sr = await mainAxios.post('/teams', stringifiedData)
      //console.log("sr: ", sr)
      const jsonSr = JSON.parse(sr.data)
      console.log('jsonsr', jsonSr)
      return {
        isSuccess: true,
        message: jsonSr.message,
        teamId: jsonSr.team_id,
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

  static async deleteTeamMember(teamId, userId, userEmail) {
    try {
      const sr = await mainAxios.delete(`/teams/${teamId}/users/${userId}`, {
        params: { team_id: teamId, user_id: userId },
      })
      //console.log("sr: ", sr)
      const jsonSr = JSON.parse(sr.data)
      console.log('jsonsr', jsonSr)
      return {
        isSuccess: true,
        message: jsonSr.message,
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
