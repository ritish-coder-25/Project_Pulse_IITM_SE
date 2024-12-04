<template>
  <div>
    <!-- Loading Indicator -->
    <div v-if="loading" class="loading">
      Loading team data, please wait...
    </div>
    <div v-else>
      <!-- Team Dashboard Header -->
      <div class="dashboard-header">
        <h3>Welcome, {{ user_name }}</h3>
        <div class="team-info">
          <p>You belong to {{ team_name }}</p>
          <p>Team's Score: {{ team_score }}/{{ total_max_marks }}</p>
        </div>
        <h5>Team Details</h5>
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
        <h4 class="mb-3">Milestone Status</h4>
        <table class="milestone-table table text-center table-bordered table-striped">
          <thead>
            <tr>
              <th>MILESTONES</th>
              <th v-for="milestone in milestone_items" :key="milestone.milestone_name">{{ milestone.milestone_name }}</th>
            </tr>
          </thead>
          <tbody>
            <tr>
              <td>Deadline</td>
              <td v-for="milestone in milestone_items" :key="milestone.end_date">{{ milestone.end_date }}</td>
            </tr>
            <tr>
              <td>Status</td>
              <td v-for="milestone in milestone_items" :key="milestone.completion_status">{{ milestone.milestone_status }}</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  </div>
</template>

<script>
import axios from "axios";
import EasyDataTable from "vue3-easy-data-table";
import "vue3-easy-data-table/dist/style.css";
import { LocalStorageEnums } from '@/enums';

export default {
  name: "StudentTeamsDashboard",
  components: {
    EasyDataTable,
  },
  data() {
    return {
      loading: true,
      error: null,
      user_name: "",
      team_name: "",
      team_score: 0,
      total_max_marks: 0,
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
  mounted() {
    this.fetchTeamData();
  },
  methods: {
    async fetchTeamData() {
      const u_id = this.$route.params.u_id;

      if (!u_id) {
        this.error = "User ID not found. Please try again.";
        this.loading = false;
        return;
      }

      try {
        const response = await axios.get(`http://localhost:5000/api/stu_home/${u_id}`, {
          headers: {
            "Content-Type": "application/json",
            Authorization: `Bearer ${localStorage.getItem(LocalStorageEnums.accessToken)}`,
          },
        });

        const { user_name, team_name, team_score, total_max_marks, members, milestones } = response.data;

        this.user_name = user_name;
        this.team_name = team_name;
        this.team_score = team_score;
        this.total_max_marks = total_max_marks;

        this.stu_items = members.map((member) => ({
          stu_name: member.name,
          stu_email: member.email,
          commit_count: member.commit_count,
        }));

        this.milestone_items = milestones.map((milestone) => ({
          milestone_name: milestone.milestone_name,
          end_date: new Date(milestone.end_date).toLocaleDateString("en-US"),
          milestone_status: milestone.milestone_status,
        }));
      } catch (error) {
        console.error("Failed to fetch data from the API:", error);
        this.error = "Unable to load team data. Please try again later.";
      } finally {
        this.loading = false;
      }
    },
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
.dashboard-header {
  display: flex;
  flex-direction: column;
  align-items: center;
  width: 100%;
  margin-bottom: 20px;
  text-align: center;
}
.team-info {
  display: flex;
  justify-content: space-between;
  align-items: center;
  width: 100%;
  margin-bottom: 20px;
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
