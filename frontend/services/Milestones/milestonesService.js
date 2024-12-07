import { MileStoneStatusEnums, MileStoneStatusWebEnums } from '@/enums'
import { mainAxios } from '@/helpers'

export class MileStoneService {
  static async getMilestones() {
    try {
      const response = await mainAxios.get('/milestones')
      const milestones = JSON.parse(response.data)
      const statuses = await this.getUserMilestoneStatuses()
      const files = await this.getUserFiles()
      console.log('main files', files)
      //console.log("milestones", milestones, "statuses", statuses, "resp", response.data);
      const convertedMilestones = milestones.map(milestone => {
        const id = milestone.milestone_id
        const name = milestone.milestone_name
        const description = milestone.milestone_description
        const startDate = new Date(milestone.start_date)
        const endDate = new Date(milestone.end_date)
        const maxMarks = milestone.max_marks
        const projectId = milestone.project_id
        const milestoneStatus = this.searchMilestoneStatuses(statuses, id)
        const uploadedFiles = this.searchFiles(files, id)
        console.log('found', uploadedFiles)
        const statusObj = this.getMileStoneStatus(
          startDate,
          endDate,
          milestoneStatus,
        )
        const status = statusObj.message
        const completed = false
        const compStatus = statusObj.status
        const inputDisabled = this.getInputDisabled(compStatus)
        //console.log('inputDisabled', inputDisabled, compStatus)
        return {
          id,
          name,
          description,
          startDate,
          endDate,
          maxMarks,
          projectId,
          status,
          completed,
          compStatus,
          inputDisabled,
          uploadedFiles,
        }
      })
      return convertedMilestones
    } catch (err) {
      console.error('Error getting milestones', err)
      return
    }
  }

  static getMileStoneStatus(startDate, endDate, milestoneStatus) {
    const today = new Date()
    let message = ''
    let status = ''

    if (milestoneStatus) {
      if (
        milestoneStatus.milestone_status === MileStoneStatusWebEnums.completed
      ) {
        message = `Completed on ${new Date(
          milestoneStatus.completed_date,
        ).toDateString()}`
        status = MileStoneStatusEnums.completed
        return {
          message,
          status,
        }
      } else if (
        milestoneStatus.milestone_status === MileStoneStatusWebEnums.evaluated
      ) {
        message = `Evaluated on ${new Date(
          milestoneStatus.eval_date,
        ).toDateString()}`
        status = MileStoneStatusEnums.completed
        return {
          message,
          status,
        }
      }
    }

    if (today < startDate) {
      message = 'Not started'
      status = MileStoneStatusEnums.notStarted
    } else if (today > endDate) {
      message = `Deadline crossed: ${endDate.toDateString()}`
      status = MileStoneStatusEnums.deadlineCrossed
    } else {
      message = `Due Date: ${endDate.toDateString()}`
      status = MileStoneStatusEnums.notSubmitted
    }
    return {
      message,
      status,
    }
  }

  static getInputDisabled(status) {
    if (status === MileStoneStatusEnums.completed) {
      return true
    } else if (status === MileStoneStatusEnums.deadlineCrossed) {
      return true
    }
    return false
  }

  static async uploadFile(file, milestoneId, projectId = 1) {
    try {
      const formData = new FormData()
      formData.append('file', file)
      formData.append('milestone_id', milestoneId)
      formData.append('project_id', projectId)
      const response = await mainAxios.post(`/submit_project`, formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
        },
      })
      const result = JSON.parse(response.data)
      const message = result.message
      const filePath = result.file_path
      return { message, filePath }
    } catch (err) {
      console.error('Error uploading file', err)
      return null
    }
  }

  static async createMilestoneStatus(milestoneId, projectId = 1) {
    const data = JSON.stringify({
      milestone_id: milestoneId,
      project_id: projectId,
    })
    const response = await mainAxios.post('/milestone-status', data)
    const result = JSON.parse(response.data)
    const message = result.message
    const milestoneStatus = result.milestone_status
    return { message, milestoneStatus }
  }

  static async getUserMilestoneStatuses() {
    try {
      const response = await mainAxios.get(`/milestone-status`)
      const result = JSON.parse(response.data)
      const statuses = result.statuses
      return statuses
    } catch (err) {
      console.error('Error getting user milestone statuses', err)
      return null
    }
  }

  static async getUserFiles() {
    try {
      const response = await mainAxios.get('/uploaded-files')
      const result = JSON.parse(response.data)
      return result.documents
    } catch (err) {
      console.error('Error getting user files', err)
      return null
    }
  }

  static searchMilestoneStatuses(milestoneStatuses, id) {
    const filtered = milestoneStatuses.filter(status => {
      return status.milestone_id === id
    })
    if (filtered.length > 0) {
      return filtered[0]
    }
    return null
  }

  static searchFiles(files, id) {
    const filtered = files.filter(file => {
      return file.milestoneId === id
    })
    if (filtered.length > 0) {
      return filtered
    }
    return null
  }

  static async getOnlyMilestones() {
    try {
      const response = await mainAxios.get('/milestones')
      const milestones = JSON.parse(response.data)

      const convertedMilestones = milestones.map(milestone => {
        const id = milestone.milestone_id
        const name = milestone.milestone_name
        const description = milestone.milestone_description
        const startDate = new Date(milestone.start_date)
        const endDate = new Date(milestone.end_date)
        const maxMarks = milestone.max_marks
        const projectId = milestone.project_id
        const statusObj = this.getMileStoneStatus(startDate, endDate)
        const status = statusObj.message
        const compStatus = statusObj.status
        const inputDisabled = this.getInputDisabled(compStatus)
        return {
          id,
          name,
          description,
          startDate,
          endDate,
          maxMarks,
          projectId,
          status,
          compStatus,
          inputDisabled
        }
      })
      return convertedMilestones
    } catch (err) {
      console.error('Error getting milestones', err)
      return
    }
  }
}
