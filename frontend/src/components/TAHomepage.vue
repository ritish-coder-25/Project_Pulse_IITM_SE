<template>
  <div class="container-fluid">
    <div class="my-4">
      <h2 class="mb-4">User Approvals Pending</h2>
      <table class="table">
        <thead>
          <tr>
            <th>User</th>
            <th>Email</th>
            <th class="text-center">Approve</th>
            <th class="text-center">Decline</th>
            <th>Select Role</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="user in pendusers" :key="user.id">
            <td>{{ user.name }}</td>
            <td>{{ user.email }}</td>
            <td class="text-center">
              <input 
                type="checkbox" 
                v-model="user.approved" 
                :disabled="user.rejected" 
                @change="toggleSelection(user, 'approved')" 
              /> 
            </td>
            <td class="text-center">
              <input 
                type="checkbox" 
                v-model="user.rejected" 
                :disabled="user.approved" 
                @change="toggleSelection(user, 'rejected')" 
              /> 
            </td>
            <td>
              <select v-model="user.role" class="form-control">
                <option value="Student">Student</option>
                <option value="TA">TA</option>
              </select>
            </td>
          </tr>
          <tr class="text-right">
            <td colspan="4"></td>
            <td>
              <button @click="submitForm" class="btn btn-primary">Submit</button>
              <button @click="resetForm" class="btn btn-secondary ms-2">Cancel</button>
            </td>
          </tr>
        </tbody>
      </table>
    </div>


    <div class="my-4">
    <h2>New activities in last 7 days</h2>
    <table class="table">
      <tbody>
        <tr>
          <td style="width: 20%;">New Commits from:</td>
          <td  style="width: 80%;">{{ commits.map(commit => commit.team).join(', ') }}</td>
        </tr>
        <tr>
          <td style="width: 20%;">New document uploads from:</td>
          <td style="width: 80%;">{{ uploads.map(upload => upload.team).join(', ') }}</td>
        </tr>
        <tr>
          <td style="width: 20%;">New milestone completions from:</td>
          <td style="width: 80%;">{{ milecomps.map(milecomp => milecomp.team).join(', ') }}</td>
        </tr>
      </tbody>
    </table>
    </div>
    </div>
</template>

<script>
import { TaHomePageApiHelpers } from '@/helpers/ApiHelperFuncs/TaHomePage';

export default {
  name: 'TAHomepage',
  data() {
    return {
      pendusers: [],
      uploads: [],
      commits: [],
      milecomps: [],
    };
  },
  methods: {
    async fetchPendusers() {
      try {
        const response = await TaHomePageApiHelpers.fetchPendusers();
        this.pendusers = response.map(user => ({
        ...user,
        role: user.role || 'Student',  // Set 'Student' if role is not defined
        }));
      } catch (error) {
        console.warn("Using local pending user data due to error:", error);
      }
    },
    async fetchUploads() {
      try {
        const response = await TaHomePageApiHelpers.fetchUploads();
        this.uploads = response;
      } catch (error) {
        console.warn("Using local uploads data due to error:", error);
      }
    },
    async fetchCommits() {
      try {
        const response = await TaHomePageApiHelpers.fetchCommits();
        this.commits = response;
      } catch (error) {
        console.warn("Using local commit data due to error:", error);
      }
    },
    async fetchMilecomps() {
      try {
        const response = await TaHomePageApiHelpers.fetchMilecomps();
        this.milecomps = response;
      } catch (error) {
        console.warn("Using local milestone completion data due to error:", error);
      }
    },
    async submitForm() {
      const allChecked = this.pendusers.every(user => user.approved || user.rejected);
      if (!allChecked) {
        alert("Please select either Approve or Decline for all users.");
        return; // Exit the function if not all checkboxes are selected
      }
      const confirmed = confirm(`Are you sure you want to submit?`);
      if (confirmed) {
        alert('Form submitted!');
        this.resetForm()
        // Send data to server
      } else {
        alert('Submission canceled.');
      }
    },
    resetForm() {
      this.pendusers.forEach(user => {
        user.approved = false;
        user.rejected = false;
        user.role = '';
    });
    }
  },
  mounted() {
    this.fetchPendusers();
    this.fetchUploads();
    this.fetchCommits();
    this.fetchMilecomps();
  },
};
</script>

<style scoped>
.container {
  max-width: 700px;
}

.card-header {
  font-weight: bold;
}

.card {
  border: 1px solid #ccc;
}

.datalist {
  max-height: 200px;
  overflow-y: auto;
}
</style>
