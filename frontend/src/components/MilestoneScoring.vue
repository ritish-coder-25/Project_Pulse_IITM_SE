<script setup>
import FormConatiner from './MainComponents/FormConatiner.vue'
</script>

<template>
  <div>
    <div class="row mt-5">
      <FormConatiner>
        <h2 class="mb-4">Milestone Scoring and Review</h2>

        <!-- Team Selection -->
        <div class="form-group mb-3">
          <label for="teamSelect" class="form-label">Select Team</label>
          <input type="text" v-model="selectedTeam.name" list="teams" class="form-control"
            placeholder="Start typing team name..." id="teamSelect" @change="handleTeamChange" />
          <datalist id="teams">
            <option v-for="team in teams" :key="team.id" :value="team.name">
              {{ team.name }}
            </option>
          </datalist>
        </div>

        <!-- Milestone Selection -->
        <div class="form-group mb-3">
          <label for="milestoneSelect" class="form-label">Select Milestone</label>
          <input type="text" v-model="selectedMilestone.milestone_name" list="milestones" class="form-control"
            placeholder="Start typing milestone name..." id="milestoneSelect" @change="handleMilestoneChange" />


          <datalist id="milestones">
            <option v-for="milestone in milestones" :key="milestone.milestone_id" :value="milestone.milestone_name">
              {{ milestone_name }}
            </option>
          </datalist>
        </div>

        <!-- Row containing Documents and Feedback side-by-side -->
        <div class="row">
          <!-- Documents Column -->
          <div class="col-md-6">
            <div class="card mb-3">
              <div class="card-header bg-primary text-white">
                Documents Uploaded
              </div>
              <div class="card-body">

                <div v-if="filteredDocuments.length">
                  <a v-for="document in filteredDocuments" :key="document.id" @click="downloadDocument(document.id)"
                    class="d-block text-primary" style="cursor: pointer;">
                    {{ document.name }}
                  </a>
                </div>
                <p v-else class="text-muted mt-2">
                  No documents available for the selected team and milestone.
                </p>
              </div>
            </div>
          </div>

          <!-- Feedback Column -->
          <div class="col-md-6">
            <div class="card mb-3">
              <div class="card-header bg-secondary text-white">
                Code Feedback
              </div>
              <div class="card-body">
                <p class="card-text">
                  {{ feedback || 'No feedback provided.' }}
                </p>
                <textarea v-model="feedback" class="form-control mt-2" rows="3"
                  placeholder="Add additional feedback if needed"></textarea>
              </div>
            </div>
          </div>
        </div>

        <!-- Score and Buttons -->
        <div class="row g-3">
          <div class="col-md-6">
            <div class="form-group">
              <label for="teamScore" class="form-label">Team Score</label>
              <input type="number" v-model.number="teamScore" class="form-control" placeholder="Enter score"
                id="teamScore" />
            </div>
          </div>
          <div class="col-md-6">
            <div class="form-group">
              <label for="maxMilestoneScore" class="form-label">Max Milestone Score</label>
              <input type="number" v-model="maxMilestoneScore" class="form-control" id="maxMilestoneScore" readonly />
            </div>
          </div>
        </div>

        <div class="d-flex mt-4">
          <button type="button" @click="submitForm" class="btn btn-primary">Submit</button>
          <button type="button" @click="resetForm" class="btn btn-secondary ms-2">
            Cancel
          </button>
        </div>
      </FormConatiner>
    </div>
  </div>
</template>

<script>
import { toRaw } from 'vue';
import { TaScoringApiHelpers } from '@/helpers/ApiHelperFuncs/TaScoringPage'
import TaScoringApiHelpersJson from '@/helpers/ApiHelperFuncs/TaScoringPage/TaScoringApiHelpers.json'
export default {
  name: 'MilestoneReview',
  data() {
    return {
      selectedTeam: {
        id: '',
        name: ''
      },
      selectedMilestone: {
        id: '',
        milestone_name: '',
        max_marks: 0
      },
      teams: [],
      milestones: [],
      documents: [],
      filteredDocuments: [], // To hold documents filtered by team and milestone
      feedback: '',
      teamScore: 18,
      maxMilestoneScore: 20
    }
  },
  methods: {
    async fetchTeams() {
      try {
        const response = await TaScoringApiHelpers.fetchTeams()
        console.log("Teams data received:", response.data)
        this.teams = response.data
      } catch (error) {
        console.warn('Using local teams data due to error:', error)
        this.teams = TaScoringApiHelpersJson.teams
      }
    },
    async fetchMilestones() {
      try {
        const response = await TaScoringApiHelpers.fetchMilestones()
        console.log("Milestones data received:", response.data)
        this.milestones = response.data.milestones;

      } catch (error) {
        console.warn('Using local milestones data due to error:', error)
        this.milestones = TaScoringApiHelpersJson.milestones
      }
    },
    async fetchDocuments() {
      try {
        this.maxMilestoneScore = this.selectedMilestone.max_marks
        const response = await TaScoringApiHelpers.fetchDocs(this.selectedTeam.id)
        this.documents = Array.isArray(response.data) ? response.data : []
        console.log("Documents ye rha:", this.documents)
        this.filterDocuments()
      } catch (error) {
        console.warn('Using local documents data due to error:', error)
        this.documents = TaScoringApiHelpersJson.documents
        this.filterDocuments()
      }
    },
    filterDocuments() {
      // Only filter if both team and milestone are selected
      if (this.selectedTeam.name && this.selectedMilestone.milestone_name) {
        this.filteredDocuments = this.documents.filter(doc =>
          doc.team === this.selectedTeam.name &&
          doc.milestone === this.selectedMilestone.milestone_name
        )
        console.log("Filtered documents:", this.filteredDocuments)
      }
    },
    handleTeamChange(event) {
      const teamName = event.target.value
      const team = this.teams.find(t => t.name === teamName)
      if (team) {
        this.selectedTeam = team
        this.filterDocuments()
      }
    },
    handleMilestoneChange(event) {
      const milestoneName = event.target.value
      const milestone = this.milestones.find(m => m.milestone_name === milestoneName)
      if (milestone) {
        this.selectedMilestone = milestone
        this.maxMilestoneScore = milestone.max_marks
        this.fetchDocuments()
        // this.filterDocuments()
      }
    },
    async submitForm() {
      const rawSelectedTeam = toRaw(this.selectedTeam);

      const rawSelectedMilestone = toRaw(this.selectedMilestone);
      console.log(
        "Submitting form with data:",
        rawSelectedTeam,
        rawSelectedMilestone,
        this.teamScore,
        this.feedback
      );


      if (!rawSelectedTeam.id || !rawSelectedMilestone.milestone_id) {
        alert("Please select a valid team and milestone.");
        return;
      }

      if (this.teamScore > this.maxMilestoneScore) {
        alert("Team Score cannot exceed the Max Milestone Score.");
        return;
      }
      const payload = {
        team_id: rawSelectedTeam.id,
        team_score: this.teamScore,
        milestone_id: rawSelectedMilestone.milestone_id,
        feedback: this.feedback,
        max_milestone_score: this.maxMilestoneScore,
      };

      console.log("Payload: ", payload);
      try {
        const response = await TaScoringApiHelpers.submitMilestoneReview(payload);
        alert(response.message || "Milestone review saved successfully.");
        this.resetForm(); // Reset form on success
      } catch (error) {
        console.error("Error submitting milestone review:", error);
        const message =
          error?.message ||
          "An unexpected error occurred while submitting the review.";
        alert(message);
      }
    },
    resetForm() {
      this.selectedTeam = {
        id: '',
        name: ''
      }
      this.selectedMilestone = {
        id: '',
        milestone_name: '',
        max_marks: 0
      }
      this.feedback = ''
      this.teamScore = null
      this.filteredDocuments = []
    },
    async downloadDocument(fileId) {
      try {
        const response = await TaScoringApiHelpers.downloadFile(fileId)
        const url = window.URL.createObjectURL(new Blob([response.data]))
        const link = document.createElement('a')
        link.href = url
        link.target = '_blank'
        document.body.appendChild(link)
        link.click()
        document.body.removeChild(link)
        window.URL.revokeObjectURL(url)
      } catch (error) {
        console.error('Error downloading file:', error)
      }
    },
  },
  mounted() {
    this.fetchTeams()
    this.fetchMilestones()
    // this.fetchDocuments()
  },
  computed: {
    maxMilestoneScore() {
      return this.selectedMilestone.max_marks || 0

    }
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
