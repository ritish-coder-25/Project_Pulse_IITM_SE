import { MileStoneStatusEnums } from '@/enums'
import { mainAxios } from '@/helpers'

export class MileStoneService {
  static async getMilestones() {
    try {
      const response = await mainAxios.get('/milestones')
      const milestones = JSON.parse(response.data).milestones
      //console.log("milestones", response.data.milestones)
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
        const completed = false
        const compStatus = statusObj.status
        const inputDisabled = this.getInputDisabled(compStatus)
        console.log('inputDisabled', inputDisabled, compStatus)
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
        }
      })
      return convertedMilestones
    } catch (err) {}
  }

  static getMileStoneStatus(startDate, endDate) {
    const today = new Date()
    let message = ''
    let status = ''
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
      return null;
    }
  }
}

// {
//     "milestones": [
//         {
//             "end_date": "Sun, 01 Dec 2024 00:00:00 GMT",
//             "max_marks": 10.0,
//             "milestone_description": "The first milestone",
//             "milestone_id": 1,
//             "milestone_name": "Milestone 1",
//             "project_id": 1,
//             "start_date": "Sun, 01 Dec 2024 00:00:00 GMT"
//         },
//         {
//             "end_date": "Thu, 05 Dec 2024 00:00:00 GMT",
//             "max_marks": 10.0,
//             "milestone_description": "The second milestone",
//             "milestone_id": 2,
//             "milestone_name": "Milestone 2",
//             "project_id": 1,
//             "start_date": "Tue, 03 Dec 2024 00:00:00 GMT"
//         },
//         {
//             "end_date": "Sun, 08 Dec 2024 00:00:00 GMT",
//             "max_marks": 10.0,
//             "milestone_description": "The third milestone",
//             "milestone_id": 3,
//             "milestone_name": "Milestone 3",
//             "project_id": 1,
//             "start_date": "Fri, 06 Dec 2024 00:00:00 GMT"
//         }
//     ]
// }
