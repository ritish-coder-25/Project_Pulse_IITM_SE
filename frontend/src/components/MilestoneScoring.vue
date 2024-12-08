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

        <!-- Trigger Celery Task Button -->
        <div class="form-group mb-3">
          <button type="button" v-if="!hideButton" @click="startCeleryTask" class="btn btn-warning">Trigger Celery Task</button>
        </div>

        <div v-if="hideButton" class="loading-container">
      <div class="loading-spinner"></div>
      <p> ⌛ Loading Commits and Generating Reports... Please wait.</p>
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
                  <a v-for="document in filteredDocuments" :key="document.id" :href="document.url" target="_blank"
                    class="d-block text-primary" style="cursor: pointer;">
                    {{
                      document.name.length > 30
                        ? document.name.slice(0, 15) + '...' + document.name.slice(-15)
                        : document.name
                    }}
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

        <!-- Commits Section -->
        <div class="row mt-4">
          <div class="col-md-12">
            <div class="card mb-3 shadow">
              <!-- Card Header -->
              <div class="card-header bg-primary text-white d-flex justify-content-between align-items-center">
                <h4 class="mb-0">
                  🚀 Commits
                </h4>
                <span class="badge bg-warning text-dark">{{ commits.length }} Total</span>
              </div>

              <!-- Card Body -->
              <div class="card-body">
                <ul v-if="commits.length" class="list-group">
                  <li v-for="commit in commits" :key="commit.commit_id"
                    class="list-group-item mb-3 border rounded shadow-sm">
                    <!-- Commit Header -->
                    <div class="d-flex justify-content-between align-items-center">
                      <h5 class="mb-1 text-success">
                        ✏️ {{ commit.commit_message }}
                      </h5>
                      <button class="btn btn-sm btn-outline-primary" type="button" @click="toggleCodeChanges(commit)">
                        {{ commit.showChanges ? '🙈 Hide Changes' : '👀 Show Changes' }}
                      </button>
                    </div>

                    <!-- Commit Details -->
                    <small class="text-muted">
                      🔑 <strong>Hash:</strong> {{ commit.commit_hash }} |
                      📅 <strong>Date:</strong> {{ commit.commit_date }}
                    </small>
                    <p class="mt-2 mb-1">
                      📊 <strong>Score:</strong> {{ commit.commit_score }} |
                      💡 <strong>Clarity:</strong> {{ commit.commit_clarity }} |
                      🧮 <strong>Complexity:</strong> {{ commit.complexity_score }} |
                      🎯 <strong>Quality:</strong> {{ commit.code_quality_score }}
                    </p>
                    <p>
                      💡 <strong>Suggestions:</strong>
                      <span v-if="commit.improvement_suggestions.length">
                        {{ commit.improvement_suggestions}}
                      </span>
                      <span v-else>
                        No suggestions available.
                      </span>
                    </p>

                    <!-- Expandable Code Changes -->
                    <div v-if="commit.showChanges" class="mt-3">
                      <div class="card bg-light border-info">
                        <div class="card-header text-info">
                          🛠️ Code Changes
                        </div>
                        <pre class="card-body p-3 rounded bg-white">
                  <code>{{ commit.commit_changes }}</code>
                </pre>
                      </div>
                    </div>
                  </li>
                </ul>
                <p v-else class="text-muted text-center">
                  😔 No commits available for the selected team and milestone.
                </p>
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
<!-- 
        <div v-if="reviewData" class="mt-4">
          <h3>Code Review Scores and Comments</h3>
          <pre>{{ reviewData }}</pre>
        </div> -->


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
      maxMilestoneScore: 20,
      reviewData: null,
      commits: [],
      hidebutton: false,
    }
  },
  methods: {
    toggleCodeChanges(commit) {
      if (commit.hasOwnProperty('showChanges')) {
        commit.showChanges = !commit.showChanges;
      } else {
        // Add `showChanges` property dynamically
        commit.showChanges = true;
      }
    },
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
    async fetchCommits() {
      try {
        const startDate = this.selectedMilestone.start_date
        const endDate = this.selectedMilestone.end_date
        const response = await TaScoringApiHelpers.fetchCommits({ startDate: startDate, endDate: endDate })
        console.log("Commits data received:", response.data)
        this.commits = response.data
      } catch (error) {
        console.warn('Using local teams data due to error:', error)
        this.commits = TaScoringApiHelpersJson.commits
      }
    },
    async startCeleryTask() {
      try {
        const startDate = this.selectedMilestone.start_date
        const endDate = this.selectedMilestone.end_date
        const team_id = this.selectedTeam.id
        const response = await TaScoringApiHelpers.startCeleryTask({startTime: startDate, endTime: endDate,teamId: team_id })
        console.log("Celery task started:", response)
        this.hidebutton = true;
        alert('Celery task started successfully!')
        
        const taskId = response.task_id;
        console.log("Task ID:", taskId)
        this.pollTaskStatus(taskId);
      } catch (error) {
        console.warn('Error starting Celery task:', error)
      }
    },
    async pollTaskStatus(taskId) {
      try {
        const response = await TaScoringApiHelpers.getTaskStatus(taskId);

        console.log("Polling Response:", response.data)
        if (response.data.state === 'SUCCESS') {
          alert('Celery task completed successfully!');
          this.isTaskRunning = false; // Re-enable the button
        } else if (response.data.state === 'FAILURE') {
          alert('Celery task failed.');
          this.isTaskRunning = false; // Re-enable the button
        } else {
          // Continue polling if the task is still running
          setTimeout(() => this.pollTaskStatus(taskId), 2000);
        }
      } catch (error) {
        console.warn('Error polling task status:', error);
        this.isTaskRunning = false; // Re-enable the button in case of error
      }
    },

    async fetchMilestones() {
      try {
        const response = await TaScoringApiHelpers.fetchMilestones()
        console.log("Milestones data received:", response.data)
        console.log("Milestone data received render --> :", response.data);
        this.milestones = response.data;

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
        this.reviewData = `Here's the JSON object with the requested code review scores and comments:\n\n\`\`\`json\n{\n  "code_clarity": 5,\n  "functionality": 5,\n  "efficiency": 5,\n  "maintainability": 5,\n  "documentation": 1,\n  "overall_review": {\n    "strengths": "The code changes are very clear and functional, with good efficiency and maintainability. However, there is a lack of documentation that could hinder understanding the purpose and implementation of the changes.",\n    "weaknesses": "The code lacks documentation, which can make it difficult for other developers to understand the purpose and implementation of the changes. Adding comments and explanations to the code will greatly improve its maintainability and readability.",\n    "suggested_improvements": [\n      "Add comments and explanations to the code to improve documentation.",\n      "Consider breaking down large functions into smaller, more manageable ones for better maintainability."\n    ]\n  }\n}\n\`\`\`\n\nThe code changes are well-implemented, clear, and functional, with good efficiency. However, there is a significant lack of documentation, which can make it difficult for other developers to understand the purpose and implementation of the changes. Adding comments and explanations to the code will greatly improve its maintainability and readability.`;
        this.fetchCommits()
      } catch (error) {
        console.warn('Using local documents data due to error:', error)
        this.documents = TaScoringApiHelpersJson.documents
        this.filterDocuments()
      }
    },
    filterDocuments() {
      // Only filter if both team and milestone are selected
      if (this.selectedMilestone.milestone_id) {
        this.filteredDocuments = this.documents.filter(doc =>
          // doc.team === this.selectedTeam.name &&
          doc.milestone === this.selectedMilestone.milestone_id
        )
        // console.log("Filtered documents:", this.filteredDocuments)
        // console.log(this.documents, this.documents.filter(doc =>
        //   // doc.team === this.selectedTeam.name &&
        //   doc.milestone === this.selectedMilestone.milestone_id
        // ))
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
/* .container {
  max-width: 700px;
} */

.card-header {
  font-weight: bold;
}

.card {
  border: 1px solid #ccc;
}

.datalist {
  /* max-height: 200px; */
  overflow-y: auto;
}

.list-group-item {
  border: 1px solid #ddd;
  border-radius: 0.5rem;
}

pre {
  white-space: pre-wrap;
  word-wrap: break-word;
  font-size: 0.9rem;
  font-family: 'Courier New', Courier, monospace;
}
</style>
