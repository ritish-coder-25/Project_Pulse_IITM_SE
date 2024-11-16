<template>
  <div class="container mt-4 p-4 border border rounded">
    <!-- Team Dashboard Header -->
    <div style="display: flex; justify-content: center; align-items: center; width: 100%;">
      <h4>Team name: {{ team.team_name }}</h4>
      <p style="margin-left: auto;">Team's Score: {{ team_score }}/{{ team_max_score }}</p>
    </div>

    <!-- Student Data Table -->
    <div class="table-spacing">
      <EasyDataTable :headers="stu_headers" :items="stu_items" :hide-footer="true" :alternating="true"
        body-text-direction="center" header-text-direction="center" table-class-name="customize-table" />
    </div>

    <!-- Milestone Data Table -->
    <!-- <div class="table-spacing">
        <EasyDataTable
          :headers="milestone_headers"
          :items="milestone_items"
          :hide-footer="true"
          :alternating="true"
          body-text-direction="center"
          header-text-direction="center"
          table-class-name="customize-table"
        />
      </div> -->

    <h4 class="mb-3">Milestones</h4>
    <table class="milestone-table table text-center table-bordered table-striped">
      <thead>
        <tr>
          <th v-for="milestone in milestone_data">{{ milestone.milestone_name }}</th>
        </tr>
      </thead>
      <tbody>
        <tr>
          <td v-for="milestone in milestone_data">{{ milestone.end_date }}</td>
        </tr>
        <tr>
          <td v-for="milestone in milestone_data">{{ milestone.completion_status }}</td>
        </tr>
        <tr>
          <td v-for="milestone in milestone_data">
            <a v-if="milestone.eval_link" :href="milestone.eval_link">
              {{ milestone.evaluation_status }}
            </a>
            <div v-else>{{ milestone.evaluation_status }}</div>
          </td>
        </tr>
      </tbody>
    </table>

  </div>
</template>

<script>
import axios from 'axios';
import EasyDataTable from 'vue3-easy-data-table';
import 'vue3-easy-data-table/dist/style.css';
import moment from 'moment';

export default {
  name: 'StudentTeamsDashboard',
  components: {
    EasyDataTable,
  },
  data() {
    return {
      milestones: [],
      milestone_data: [],
      team: {},
      team_score: 0,
      team_max_score: 0,
      stu_headers: [
        { text: "STUDENT NAME", value: "stu_name" },
        { text: "STUDENT EMAIL", value: "stu_email" },
        { text: "NUMBER of COMMITS", value: "commits_count" },
      ],
      stu_items: [],
    };
  },
  methods: {
    formatDate(value) {
      if (value) {
        // return moment(String(value)).format('MM/DD/YYYY hh:mm')
        return moment(String(value)).format("DD-MM-YYYY")
      }
    },
    async fetchDashboardData() {
      try {
        const response = await axios.get('http://localhost:5000/api/ta-teams/' + this.$route.params.id,
          { "headers": { "Content-Type": "application/json", "Authorization": "Bearer " + localStorage.getItem("access_token") } }
        );
        this.stu_items = response.data.members;
        this.milestones = response.data.milestones;
        this.team = response.data.team;
      } catch (error) {
        console.warn("Error while fetching data:", error);
      }
    },

    async create_team_dashboard() {
      await this.fetchDashboardData();

      this.stu_headers = [
        { text: "STUDENT NAME", value: "name" },
        { text: "STUDENT EMAIL", value: "email" },
        { text: "NUMBER of COMMITS", value: "commits" },
      ];

      let milestone_statuses = {}
      let team_score = 0
      let team_max_score = 0

      for (let status of this.team.milestone_statuses) {
        milestone_statuses[status.milestone_id] = status;
      }

      for (let milestone of this.milestones) {
        let completion_status = "NA"
        let evaluation_status = "NA"
        let eval_link = null

        let ms = milestone_statuses[milestone.milestone_id]

        if (ms.milestone_status === "Completed") {
          if (ms.completed_date) {
            completion_status = "Completed on " + this.formatDate(ms.completed_date)
            eval_link = "/dashboard/instructor/milestones"
          }
          evaluation_status = "Pending Evaluation"
        } else if (ms.milestone_status === "Missed") {
          completion_status = "Milestone Missed"
          team_score += 0
          team_max_score += milestone.max_marks
        } else if (ms.milestone_status === "Evaluated") {
          if (ms.completed_date) {
            completion_status = "Completed on " + this.formatDate(ms.completed_date)
          }
          evaluation_status = "Evaluated: " + ms.eval_score + " / " + milestone.max_marks
          team_score += ms.eval_score
          team_max_score += milestone.max_marks
        }

        this.milestone_data.push({
          "milestone_id": milestone.milestone_id,
          "milestone_name": milestone.milestone_name,
          "end_date": this.formatDate(milestone.end_date),
          "milestone_status": ms.milestone_status,
          "completion_status": completion_status,
          "evaluation_status": evaluation_status,
          "eval_link": eval_link
        })
      }
      this.team_score = team_score
      this.team_max_score = team_max_score
    }

  },
  mounted() {
    this.create_team_dashboard();
  },
};
</script>

<style scoped>
.milestone-table {
  font-size: 0.75rem;
}

.table-spacing {
  margin-bottom: 50px;
}

a {
  text-decoration: none;
}
</style>