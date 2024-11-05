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
}
