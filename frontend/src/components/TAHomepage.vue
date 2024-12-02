<template>
  <div>
    <div class="row mt-5">
      <div class="mx-auto p-4 shadow-sm rounded form-container border">
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
                    <button @click="submitForm" class="btn btn-primary">
                      Submit
                    </button>
                    <button @click="resetForm" class="btn btn-secondary ms-2">
                      Cancel
                    </button>
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
                  <td style="width: 20%">New Commits from:</td>
                  <td style="width: 80%">
                    {{ commits.map(commit => commit.team).join(', ') }}
                  </td>
                </tr>
                <tr>
                  <td style="width: 20%">New document uploads from:</td>
                  <td style="width: 80%">
                    {{ uploads.map(upload => upload.team).join(', ') }}
                  </td>
                </tr>
                <tr>
                  <td style="width: 20%">New milestone completions from:</td>
                  <td style="width: 80%">
                    {{ milecomps.map(milecomp => milecomp.team).join(', ') }}
                  </td>
                </tr>
              </tbody>
            </table>
          </div>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { TaHomePageApiHelpers } from '@/helpers/ApiHelperFuncs/TaHomePage'

export default {
  name: 'TAHomepage',
  data() {
    return {
      pendusers: [],
      uploads: [],
      commits: [],
      milecomps: [],
    }
  },
  methods: {
    async fetchPendusers() {
      try {
        const response = await TaHomePageApiHelpers.fetchPendusers()
        const parsedResponse = typeof response === "string" ? JSON.parse(response) : response;
        this.pendusers = parsedResponse.map((user) => ({
          ...user,
          role: user.role || 'Student', // Set 'Student' if role is not defined
        }))
      } catch (error) {
        console.warn('Using local pending user data due to error:', error)
      }
    },
    async fetchUploads() {
      try {
        const response = await TaHomePageApiHelpers.fetchUploads()
        const parsedResponse = typeof response === "string" ? JSON.parse(response) : response;
        this.uploads = parsedResponse || []
      } catch (error) {
        console.warn('Using local uploads data due to error:', error)
      }
    },
    async fetchCommits() {
      try {
        const response = await TaHomePageApiHelpers.fetchCommits()
        const parsedResponse = typeof response === "string" ? JSON.parse(response) : response;
        this.commits = parsedResponse || []
      } catch (error) {
        console.warn('Using local commit data due to error:', error)
      }
    },
    async fetchMilecomps() {
      try {
        const response = await TaHomePageApiHelpers.fetchMilecomps()
        const parsedResponse = typeof response === "string" ? JSON.parse(response) : response;
        this.milecomps = parsedResponse
      } catch (error) {
        console.warn(
          'Using local milestone completion data due to error:',
          error,
        )
      }
    },
    async submitForm() {
      // Ensure all users have been approved or rejected
      if (!this.pendusers.every(user => user.approved || user.rejected)) {
        alert('Please select either Approve or Decline for all users.');
        return;
      }
      // Confirm submission
      if (!confirm('Are you sure you want to submit?')) {
        alert('Submission canceled.');
        return;
      }
      // Prepare and submit the payload
      try {
        const payload = {
          users: this.pendusers.map(user => ({
            user_id: user.id,
            approval_status: user.approved ? 'Approved' : 'Declined',
            user_type: user.role,
          })),
        };
        const response = await TaHomePageApiHelpers.approveUsers(JSON.stringify(payload));
        console.log('Server response:', response);
        const parsedresponse = JSON.parse(response);
        if (parsedresponse?.message === 'User approvals processed successfully') {
          alert('Form submitted successfully!');
          this.resetForm();
        } else {
          alert('Failed to submit the form. Please try again.');
        }
      } catch (error) {
        console.error('Error during form submission:', error);
        alert('An error occurred. Please try again.');
      }
    },

    resetForm() {
      window.location.reload(); 
    },
  },
  mounted() {
    this.fetchPendusers()
    this.fetchUploads()
    this.fetchCommits()
    this.fetchMilecomps()
  },
}
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
