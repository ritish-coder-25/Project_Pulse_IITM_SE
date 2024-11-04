<template>
  <div class="container mt-4 p-4 border rounded">
    <h2 class="mb-4">Milestone Scoring and Review</h2>

    <!-- Team Selection -->
    <div class="form-group mb-3">
      <label for="teamSelect" class="form-label">Select Team</label>
      <input 
        type="text" 
        v-model="selectedTeam" 
        list="teams" 
        class="form-control" 
        placeholder="Start typing team name..." 
        id="teamSelect"
        @change="filterDocuments"
      />
      <datalist id="teams">
        <option v-for="team in teams" :key="team.id" :value="team.name">{{ team.name }}</option>
      </datalist>
    </div>

    <!-- Milestone Selection -->
    <div class="form-group mb-3">
      <label for="milestoneSelect" class="form-label">Select Milestone</label>
      <input 
        type="text" 
        v-model="selectedMilestone" 
        list="milestones" 
        class="form-control" 
        placeholder="Start typing milestone name..." 
        id="milestoneSelect"
        @change="filterDocuments"
      />
      <datalist id="milestones">
        <option v-for="milestone in milestones" :key="milestone.id" :value="milestone.name">{{ milestone.name }}</option>
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
              <a 
                v-for="document in filteredDocuments" 
                :key="document.id" 
                :href="document.url" 
                target="_blank" 
                class="d-block text-primary"
              >
                {{ document.name }}
              </a>
            </div>
            <p v-else class="text-muted mt-2">No documents available for the selected team and milestone.</p>
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
            <p class="card-text">{{ feedback || "No feedback provided." }}</p>
            <textarea 
              v-model="feedback" 
              class="form-control mt-2" 
              rows="3" 
              placeholder="Add additional feedback if needed"
            ></textarea>
          </div>
        </div>
      </div>
    </div>

    <!-- Score and Buttons -->
    <div class="row g-3">
      <div class="col-md-6">
        <div class="form-group">
          <label for="teamScore" class="form-label">Team Score</label>
          <input 
            type="number" 
            v-model.number="teamScore" 
            class="form-control" 
            placeholder="Enter score" 
            id="teamScore"
          />
        </div>
      </div>
      <div class="col-md-6">
        <div class="form-group">
          <label for="maxMilestoneScore" class="form-label">Max Milestone Score</label>
          <input 
            type="number" 
            v-model="maxMilestoneScore" 
            class="form-control" 
            id="maxMilestoneScore" 
            readonly 
          />
        </div>
      </div>
    </div>

    <div class="d-flex mt-4">
      <button @click="submitForm" class="btn btn-primary">Submit</button>
      <button @click="resetForm" class="btn btn-secondary ms-2">Cancel</button>
    </div>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: 'MilestoneReview',
  data() {
    return {
      selectedTeam: '',
      selectedMilestone: '',
      teams: [],
      milestones: [],
      documents: [],
      filteredDocuments: [], // To hold documents filtered by team and milestone
      feedback: '',
      teamScore: 18,
      maxMilestoneScore: 20,
      // Local fallback data
      localTeams: [
        { id: 1, name: 'Team A' },
        { id: 2, name: 'Team B' },
        { id: 3, name: 'Team C' },
      ],
      localMilestones: [
        { id: 1, name: 'Milestone 1' },
        { id: 2, name: 'Milestone 2' },
        { id: 3, name: 'Milestone 3' },
      ],
      localDocuments: [
        { id: 1, name: 'Document X_TeamA_Milestone1', url: '#', team: 'Team A', milestone: 'Milestone 1' },
        { id: 7, name: 'Document Y_TeamA_Milestone1', url: '#', team: 'Team A', milestone: 'Milestone 1' },
        { id: 2, name: 'Document Y_TeamB_Milestone2', url: '#', team: 'Team B', milestone: 'Milestone 2' },
        { id: 3, name: 'Document Z_TeamC_Milestone3', url: '#', team: 'Team C', milestone: 'Milestone 3' },
        { id: 4, name: 'Document P_TeamA_Milestone2', url: '#', team: 'Team A', milestone: 'Milestone 2' },
        { id: 5, name: 'Document Q_TeamB_Milestone3', url: '#', team: 'Team B', milestone: 'Milestone 3' },
        { id: 6, name: 'Document R_TeamC_Milestone1', url: '#', team: 'Team C', milestone: 'Milestone 1' },
        // Add more document data here as needed
      ],
    };
  },
  methods: {
    async fetchTeams() {
      try {
        const response = await axios.get('http://localhost:3000/teams');
        this.teams = response.data;
      } catch (error) {
        console.warn("Using local teams data due to error:", error);
        this.teams = this.localTeams;
      }
    },
    async fetchMilestones() {
      try {
        const response = await axios.get('http://localhost:3000/milestones');
        this.milestones = response.data;
      } catch (error) {
        console.warn("Using local milestones data due to error:", error);
        this.milestones = this.localMilestones;
      }
    },
    async fetchDocuments() {
      try {
        const response = await axios.get('http://localhost:3000/documents');
        this.documents = response.data;
        this.filterDocuments();
      } catch (error) {
        console.warn("Using local documents data due to error:", error);
        this.documents = this.localDocuments;
        this.filterDocuments();
      }
    },
    filterDocuments() {
      this.filteredDocuments = this.documents.filter(
        (doc) =>
          doc.team === this.selectedTeam && doc.milestone === this.selectedMilestone
      );
    },
    async submitForm() {
      alert(`Form submitted with Team Score: ${this.teamScore} / ${this.maxMilestoneScore}`);
      // Add form submission handling here
    },
    resetForm() {
      this.selectedTeam = '';
      this.selectedMilestone = '';
      this.feedback = '';
      this.teamScore = null;
      this.filteredDocuments = [];
    },
  },
  mounted() {
    this.fetchTeams();
    this.fetchMilestones();
    this.fetchDocuments();
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
