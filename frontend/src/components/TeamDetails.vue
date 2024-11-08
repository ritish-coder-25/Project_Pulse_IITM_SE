<template>
    <div class="container mt-4 p-4 border border rounded">
      <!-- Team Dashboard Header -->
      <div style="display: flex; justify-content: center; align-items: center; width: 100%;">
        <h3>Team name: Team {{ $route.params.id }}</h3>
        <p style="margin-left: auto;">Team's Score: 80/100</p>
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
  import axios from 'axios';
  import EasyDataTable from 'vue3-easy-data-table';
  import 'vue3-easy-data-table/dist/style.css';
  
  export default {
    name: 'StudentTeamsDashboard',
    components: {
      EasyDataTable,
    },
    data() {
      return {
        stu_headers: [
          { text: "STUDENT NAME", value: "stu_name" },
          { text: "STUDENT EMAIL", value: "stu_email" },
          { text: "NUMBER of COMMITS", value: "number" },
        ],
        stu_items: [],
        milestone_headers: [
          { text: "MILESTONES", value: "details" },
          { text: "Milestone 1", value: "milestone1" },
          { text: "Milestone 2", value: "milestone2" },
          { text: "Milestone 3", value: "milestone3" },
          { text: "Milestone 4", value: "milestone4" },
          { text: "Milestone 5", value: "milestone5" },
          { text: "Milestone 6", value: "milestone6" },
        ],
        milestone_items: [],
        localStuData: [
          { id: 1, stu_name: "Stephen Curry", stu_email: "21f1001234@mail.com" },
          { id: 2, stu_name: "Lebron James", stu_email: "21f1004321@mail.com" },
          { id: 3, stu_name: "Kevin Durant", stu_email: "21f1001212@mail.com" },
          { id: 4, stu_name: "Giannis Antetokounmpo", stu_email: "21f1001213@mail.com" },
        ],
        localStuCommits: [
          { user_id: 1, commits: 20 },
          { user_id: 2, commits: 19 },
          { user_id: 3, commits: 22 },
          { user_id: 4, commits: 17 },
        ],
        localMilestones: [
          { details: "Deadline", milestone1: "20 Oct 2024", milestone2: "20 Oct 2024", milestone3: "10 Nov 2024", milestone4: "17 Nov 2024", milestone5: "24 Nov 2024", milestone6: "01 Dec 2024" },
          { details: "Status", milestone1: "Missed", milestone2: "Completed", milestone3: "Pending", milestone4: "Pending", milestone5: "Pending", milestone6: "Pending" },
          {details: "Evaluation Status",  milestone1: "Missed", milestone2: "Evaluated 80/100", milestone3: "Pending", milestone4: "Pending", milestone5: "Pending", milestone6: "Pending" }
        ],
      };
    },
    methods: {
      async fetchStuData() {
        try {
          const response = await axios.get('http://localhost:5000/{{team_id}}/student');
          this.stu_items = response.data.map(stu => {
            const commits = this.localStuCommits.find(c => c.user_id === stu.id)?.commits || 0;
            return { ...stu, number: commits };
          });
        } catch (error) {
          console.warn("Using local student data due to error:", error);
          this.stu_items = this.localStuData.map(stu => {
            const commits = this.localStuCommits.find(c => c.user_id === stu.id)?.commits || 0;
            return { ...stu, number: commits };
          });
        }
      },
      async fetchMilestones() {
        try {
          const response = await axios.get('http://localhost:5000/milestones');
          this.milestone_items = response.data;
        } catch (error) {
          console.warn("Using local milestone data due to error:", error);
          this.milestone_items = this.localMilestones;
        }
      },
    },
    mounted() {
      this.fetchStuData();
      this.fetchMilestones();
    },
  };
  </script>
  
  <style scoped>
  .table-spacing {
    margin-bottom: 50px;
  }
  </style>
  