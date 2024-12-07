<template>
  <div class="manage-milestone">
    <table class="milestone-table">
      <thead>
        <tr>
          <th>Milestone</th>
          <th>Upload Documents</th>
          <th>Mark as Complete</th>
          <th>Status</th>
        </tr>
      </thead>
      <tbody>
        <tr v-for="milestone in milestones" :key="milestone.id">
          <td>
            <!-- Link to navigate to MilestoneInfo.vue without parameters -->
            <router-link to="/milestone-info">{{ milestone.name }}</router-link>
          </td>
          <td>
            <input
              type="file"
              :disabled="milestone.inputDisabled"
              @change="handleFileUpload($event, milestone)"
            />
          </td>
          <td>
            <input
              type="checkbox"
              :disabled="milestone.inputDisabled"
              v-model="milestone.completed"
              @change="markAsComplete(milestone)"
            />
          </td>
          <td
            :class="{
              missed: milestone.status === 'Deadline missed',
              due: milestone.status.startsWith('Due Date'),
            }"
          >
            {{ milestone.status }}
          </td>
        </tr>
      </tbody>
    </table>

    <div class="note">
      <p>
        <strong>Note:</strong> Documents can be uploaded and the submit button
        can be clicked without marking the milestone as complete. Once a
        milestone is marked as completed, no further changes are allowed.
      </p>
    </div>

    <div class="actions">
      <button @click="submit" :disabled="isSubmitDisabled">Submit</button>
      <button @click="reset">Reset</button>
    </div>
  </div>
</template>

<script>
import { onMounted } from 'vue'
import { MileStoneService } from '../../services/Milestones/milestonesService'
import { MileStoneStatusEnums } from '@/enums'
import { Emitter, Events } from '@/Events'

export default {
  name: 'ManageMilestone',
  data() {
    return {
      milestones: [
        // { id: 1, name: 'Milestone 1', status: 'Completed on xxxxx', completed: true },
        // { id: 2, name: 'Milestone 2', status: 'Deadline missed', completed: false },
        // { id: 3, name: 'Milestone 3', status: 'Due Date: 10 Nov', completed: false },
        // { id: 4, name: 'Milestone 4', status: 'Not open', completed: false },
        // { id: 5, name: 'Milestone 5', status: 'Not open', completed: false },
      ],
    }
  },
  computed: {
    isSubmitDisabled() {
      return this?.milestones?.every(milestone => !milestone.completed)
    },
  },
  methods: {
    async handleFileUpload(event, milestone) {
      const file = event.target.files[0]
      if (file) {
        Emitter.emit(Events.showToast, {
          title: 'Starting upload',
          message: `File ${file.name} uploaded for ${milestone.name}`,
          variant: 'info',
        })
        const resu = await MileStoneService.uploadFile(file, milestone.id)
        if (resu) {
          Emitter.emit(Events.showToast, {
            title: 'Upload completed',
            message: `File ${file.name} uploaded for ${milestone.name}`,
            variant: 'success',
          })
        } else {
          Emitter.emit(Events.showToast, {
            title: 'Upload failed',
            message: `File ${file.name} upload failed for ${milestone.name}`,
            variant: 'danger',
          })
        }
      }
    },
    markAsComplete(milestone) {
      if (milestone.completed) {
        alert(
          `Marking ${milestone.name} as complete. No further changes allowed.`,
        )
        milestone.status = `Completed on ${new Date().toLocaleDateString()}`
      }
    },
    submit() {
      alert('Submitting changes...')
      // Logic for submit action
    },
    reset() {
      this.milestones.forEach(milestone => {
        if (!milestone.status.includes('Completed')) {
          milestone.completed = false
        }
      })
      alert('All changes have been reset.')
    },
    async fetchMilestones() {
      // Fetch milestones from API
      // this.milestones = await fetchMilestones();
      const conveMilestones = await MileStoneService.getMilestones()
      console.log('converted return milestones', conveMilestones)
      this.milestones = conveMilestones
    },
  },
  async mounted() {
    await this.fetchMilestones()
  },
}
</script>

<style scoped>
.manage-milestone {
  padding: 16px;
  font-family: Arial, sans-serif;
  background-color: #f4f6f9;
  border-radius: 8px;
  box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
}

.milestone-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 16px;
  background-color: #ffffff;
  border-radius: 8px;
  overflow: hidden;
}

.milestone-table th,
.milestone-table td {
  padding: 12px;
  border: 1px solid #ddd;
  text-align: center;
}

.milestone-table th {
  background-color: #3498db;
  color: #ffffff;
  font-weight: bold;
}

.milestone-table a {
  color: #3498db;
  text-decoration: none;
  font-weight: bold;
  transition: color 0.3s;
}

.milestone-table a:hover {
  color: #2980b9;
}

.missed {
  color: #e74c3c;
  font-weight: bold;
}

.due {
  color: #2ecc71;
  font-weight: bold;
}

.note {
  background-color: #fff8c6;
  margin-top: 16px;
  padding: 12px;
  border-radius: 4px;
  font-size: 14px;
  color: #555;
}

.actions {
  margin-top: 20px;
  text-align: center;
}

.actions button {
  background-color: #3498db;
  color: #ffffff;
  border: none;
  border-radius: 5px;
  padding: 8px 16px;
  font-size: 16px;
  cursor: pointer;
  margin-right: 8px;
  transition: background-color 0.3s;
}

.actions button:hover {
  background-color: #2980b9;
}

.actions button:disabled {
  background-color: #bdc3c7;
  cursor: not-allowed;
}
</style>
