import { mainAxios } from '@/helpers'
import { DefineTeamApiHelper } from '@/helpers/ApiHelperFuncs/DefineTeam'

export class DefineTeamService {
  static async removeEmail({
    index,
    setFieldValue,
    currentTeam,
    valuesRef,
    emailFields,
    remove,
  }) {
    const updateduserIds = Object.values(valuesRef.user_ids).filter(
      (id, i) => i !== index,
    )
    console.log('updated user ids', updateduserIds)
    //return;
    if (currentTeam && currentTeam.members[index]) {
      // const currEmailFields = [...this.emailFields]
      // console.log('email fields', this.currentTeam.members, index)
      const userId = currentTeam.members.find(
        member => member.student_email === emailFields[index].value,
      ).id
      console.log('Deleting user:', userId)
      const delUser = await DefineTeamApiHelper.deleteTeamMember(
        currentTeam.teamId,
        userId,
      )
      if (delUser.isSuccess) {
        remove(index)
        setFieldValue(`emails.${index}`, null)
        setFieldValue(`user_ids`, updateduserIds)
      } else {
        const errorMessage = delUser.error
          ? delUser.error.message
          : delUser.errorMessage
        alert('Error deleting user - ' + errorMessage)
      }
    } else {
      remove(index)
      setFieldValue(`emails.${index}`, null)
      setFieldValue(`user_ids`, updateduserIds)
    }
  }

  static async fetchTeam({
    addEmail,
    selectEmail,
    setValuesRef,
    isTeamReadOnly,
    currentTeam,
    setFieldValueRef,
  }) {
    try {
      const teamData = await DefineTeamApiHelper.getTeam()
      if (teamData && teamData.isSuccess) {
        //setValues({ ...values, team: teamData.name })
        teamData?.members.forEach((email, index) => {
          addEmail()
          selectEmail(email.student_email, email.id, index, setFieldValueRef)
        })
        setValuesRef({
          team: teamData.team,
          github_repo_url: teamData.github_repo_url,
          // Preserve existing emails or set if needed
          emails: teamData.emails.length > 0 ? teamData.emails : [''],
        })
        isTeamReadOnly = true
        currentTeam = teamData
      }
    } catch (error) {
      console.error('Error fetching team:', error)
    }
  }

  static async debounceSearch({ event, index, searchTimeout, searchResults }) {
    const searchTerm = event.target.value

    // Clear previous timeout
    if (searchTimeout) clearTimeout(searchTimeout)

    // Set new timeout
    searchTimeout = setTimeout(async () => {
      if (searchTerm.length <= 2) {
        searchResults[index] = []
        return
      }

      try {
        // Replace with your actual API endpoint
        const response = await mainAxios.get(
          `/users?student_email=${searchTerm}`,
        )
        const data = response.data
        searchResults[index] = JSON.parse(data)
      } catch (error) {
        console.error('Error fetching emails:', error)
        searchResults[index] = []
      }
    }, 300) // 300ms delay
  }
}
