<template>
  <div class="manage-milestone">
    <div class="tabs">
      <button @click="navigateTo('home')">Home</button>
      <button @click="navigateTo('dashboard')">Dashboard</button>
      <button @click="navigateTo('define-teams')">Define Teams</button>
      <button @click="navigateTo('milestone-info')">Milestone Info</button>
      <button @click="navigateTo('milestone-progress')">Milestone Progress</button>
    </div>

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
            <a href="#" @click.prevent="goToMilestoneInfo(milestone)">{{ milestone.name }}</a>
          </td>
          <td>
            <button
              :disabled="milestone.status === 'Not open'"
              @click="openUploadWindow(milestone)"
            >
              Select
            </button>
          </td>
          <td>
            <input
              type="checkbox"
              :disabled="milestone.status === 'Not open' || milestone.status.includes('Completed')"
              v-model="milestone.completed"
              @change="markAsComplete(milestone)"
            />
          </td>
          <td :class="{ 'missed': milestone.status === 'Deadline missed', 'due': milestone.status.startsWith('Due Date') }">
            {{ milestone.status }}
          </td>
        </tr>
      </tbody>
    </table>

    <div class="note">
      <p>
        <strong>Note:</strong> Documents can be uploaded and the submit button can be clicked
        without marking the milestone as complete. Once a milestone is marked as completed, no
        further changes are allowed.
      </p>
    </div>

    <div class="actions">
      <button @click="submit" :disabled="isSubmitDisabled">Submit</button>
      <button @click="reset">Reset</button>
    </div>
  </div>
</template>

<script>
export default {
  name: 'ManageMilestone',
  data() {
    return {
      milestones: [
        { id: 1, name: 'Milestone 1', status: 'Completed on xxxxx', completed: true },
        { id: 2, name: 'Milestone 2', status: 'Deadline missed', completed: false },
        { id: 3, name: 'Milestone 3', status: 'Due Date: 10 Nov', completed: false },
        { id: 4, name: 'Milestone 4', status: 'Not open', completed: false },
        { id: 5, name: 'Milestone 5', status: 'Not open', completed: false },
      ],
    };
  },
  computed: {
    isSubmitDisabled() {
      return this.milestones.every(milestone => !milestone.completed);
    },
  },
  methods: {
    navigateTo(routeName) {
      this.$router.push({ name: routeName });
    },
    goToMilestoneInfo(milestone) {
      // Logic to navigate to Milestone Info tab with relevant description
      alert(`Navigating to info for ${milestone.name}`);
      this.$router.push({ name: 'milestone-info', params: { milestoneId: milestone.id } });
    },
    openUploadWindow(milestone) {
      if (milestone.status !== 'Not open') {
        alert(`Upload window opened for ${milestone.name}`);
        // Logic to open a file upload window or modal
      }
    },
    markAsComplete(milestone) {
      if (milestone.completed) {
        alert(`Marking ${milestone.name} as complete. No further changes allowed.`);
        milestone.status = `Completed on ${new Date().toLocaleDateString()}`;
      }
    },
    submit() {
      alert('Submitting changes...');
      // Logic for submit action
    },
    reset() {
      this.milestones.forEach(milestone => {
        if (!milestone.status.includes('Completed')) {
          milestone.completed = false;
        }
      });
      alert('All changes have been reset.');
    },
  },
};
</script>

<style scoped>
.manage-milestone {
  padding: 16px;
}

.tabs button {
  margin: 0 8px;
  padding: 8px 16px;
}

.milestone-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 16px;
}

.milestone-table th, .milestone-table td {
  padding: 12px;
  border: 1px solid #ddd;
  text-align: center;
}

.milestone-table .missed {
  color: red;
}

.milestone-table .due {
  color: green;
}

.note {
  background-color: #fff8c6;
  margin-top: 16px;
  padding: 12px;
  border-radius: 4px;
}

.actions {
  margin-top: 16px;
}

.actions button {
  margin-right: 8px;
  padding: 8px 16px;
}
</style>
