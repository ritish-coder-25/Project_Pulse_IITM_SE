<template>
  <div>
    <!-- Loading Indicator -->
    <div v-if="loading" class="loading">
      Loading team data, please wait...
    </div>
    <div v-else>
      <!-- Team Dashboard Header -->
      <div style="display: flex; justify-content: center; align-items: center; width: 100%;">
        <h3>Team name: {{ team_name }}</h3>
        <p style="margin-left: auto;">Team's Score: {{ team_score }}/100</p>
      </div>

      <!-- Error Message -->
      <div v-if="error" class="error-message">
        {{ error }}
      </div>

      <!-- Student Data Table -->
      <div v-if="!error" class="table-spacing">
        <EasyDataTable
          :headers="stu_headers"
          :items="stu_items"
          :hide-footer="true"
          :alternating="true"
          body-text-direction="center"
          header-text-direction="center"
          table-class-name="customize-table"
        />
      </div>

      <!-- Milestone Data Table -->
      <div v-if="!error" class="table-spacing">
        <EasyDataTable
          :headers="milestone_headers"
          :items="milestone_items"
          :hide-footer="true"
          :alternating="true"
          body-text-direction="center"
          header-text-direction="center"
          table-class-name="customize-table"
        />
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import EasyDataTable from "vue3-easy-data-table";
import "vue3-easy-data-table/dist/style.css";

export default {
  name: "StudentTeamsDashboard",
  components: {
    EasyDataTable,
  },
  data() {
    return {
      loading: true, 
      error: null, 
      team_name: "",
      team_score: 0,
      stu_headers: [
        { text: "STUDENT NAME", value: "stu_name" },
        { text: "STUDENT EMAIL", value: "stu_email" },
        { text: "NUMBER of COMMITS", value: "commit_count" },
      ],
      stu_items: [],
      milestone_headers: [
        { text: "MILESTONE NAME", value: "milestone_name" },
        { text: "END DATE", value: "end_date" },
        { text: "STATUS", value: "milestone_status" },
      ],
      milestone_items: [],
    };
  },
  methods: {
    async fetchTeamData() {
      try {
        const stuId = this.$route.params.stu_id; 
        const response = await axios.get(`http://localhost:5000/api/stu_home/${stuId}`, {
          headers: {
            "Content-Type": "application/json",
            Authorization: "Bearer " + localStorage.getItem("access_token"),
          },
        });

        const { team_name, team_score, members, milestones } = response.data;

        // Populate team name and score
        this.team_name = team_name;
        this.team_score = team_score;

        // Populate student data
        this.stu_items = members.map((member) => ({
          stu_name: member.name,
          stu_email: member.email,
          commit_count: member.commit_count,
        }));

        // Populate milestone data
        this.milestone_items = milestones.map((milestone) => ({
          milestone_name: milestone.milestone_name,
          end_date: new Date(milestone.end_date).toLocaleDateString("en-US"),
          milestone_status: milestone.milestone_status,
        }));
      } catch (error) {
        console.error("Failed to fetch data from the API:", error);
        this.error = "Unable to load team data. Please try again later.";
      } finally {
        this.loading = false; // Stop loading state
      }
    },
  },
  mounted() {
    this.fetchTeamData();
  },
};
</script>

<style scoped>
.table-spacing {
  margin-bottom: 50px;
}
.loading {
  text-align: center;
  font-size: 18px;
  margin-top: 20px;
}
.error-message {
  color: red;
  text-align: center;
  margin: 20px 0;
}
@media (max-width: 768px) {
  h3 {
    font-size: 16px;
  }
  p {
    font-size: 14px;
  }
  .table-spacing {
    margin-bottom: 20px;
  }
}
</style>
