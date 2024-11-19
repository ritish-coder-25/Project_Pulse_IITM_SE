<template>
  <div>
    <!-- Team Dashboard Header -->
    <div style="display: flex; justify-content: center; align-items: center; width: 100%;">
      <h3>Team name: {{ team_name }}</h3>
      <p style="margin-left: auto;">Team's Score: {{ team_score }}/100</p>
    </div>

    <!-- Student Data Table -->
    <div class="table-spacing">
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
    <div class="table-spacing">
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
        const response = await axios.get("http://localhost:5000/api/team_dashboard");
        const { members, milestones, team_name, team_score } = response.data;

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
        console.warn("Failed to fetch data from the API:", error);
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
</style>
