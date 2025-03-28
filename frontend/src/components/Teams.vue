<template>
    <div class="container mt-4 p-4 border border rounded">
        <h2 class="mb-4">TA/Instructor Dashboard</h2>

        <div v-if="fetchDataError" class="alert alert-danger" role="alert">
            Something went wrong!!!
        </div>

        <!-- Teams Table -->
        <h4 class="mb-3">Teams</h4>

        <div class="table border-secondary">
            <EasyDataTable :headers="dashboard_data_headers" :items="dashboard_data_items" :hide-footer=true
                :alternating=true body-text-direction="center" header-text-direction="center"
                table-class-name="customize-table">

                <!-- team name -->
                <template #item-team_name="{ team_name, team_url }">
                    <a :href="team_url" target="_blank">{{ team_name }}</a>
                </template>

                <!-- team score -->
                <template #item-score="{ score, total_score }">
                    {{ score }} / {{ total_score }}
                </template>
            </EasyDataTable>
        </div>


        <!-- Milestone's Table -->
        <div v-if="milestones">
            <h4 class="mb-3">Deadlines</h4>
            <table class="milestone-table table text-center table-bordered table-striped">
                <thead>
                    <tr>
                        <th v-for="milestone in milestones">{{ milestone.milestone_name }}</th>
                    </tr>
                </thead>
                <tbody>
                    <tr>
                        <td v-for="milestone in milestones">Deadline: {{ milestone.end_date }}</td>
                    </tr>
                </tbody>
            </table>
        </div>
    </div>
</template>

<script>
import moment from 'moment';
import { TaTeamsDashboardApiHelpers } from '@/helpers/ApiHelperFuncs/TaTeamsDashboard'

export default {
    name: 'Teams',

    data() {

        return {

            teams: [],
            milestones: [],
            milestone_headers: [],
            milestone_items: [],
            dashboard_data_headers: [],
            dashboard_data_items: [],
            fetchDataError: false
        };

    },
    methods: {
        formatDate(value){
        if (value) {
              // return moment(String(value)).format('MM/DD/YYYY hh:mm')
              return moment(String(value)).format("DD-MM-YYYY")
          }
      },
        async fetchDashboardData() {

            const response = await TaTeamsDashboardApiHelpers.fetchTeamsData()

            if(response){
                this.teams = response.data.teams;
                this.milestones = response.data.milestones;
            }else{
                console.error("Error while fetching teams dashboard data!!")
                this.fetchDataError = true
                this.teams = null
                this.milestones = null
            }
        },
        async create_dashboard() {

            await this.fetchDashboardData();

            for(let milestone in this.milestones){
                    this.milestones[milestone].end_date = this.formatDate(this.milestones[milestone].end_date);
                }

            this.dashboard_data_headers = [
                { text: "Team Name", value: "team_name" },
                { text: "No of Commits", value: "commits" },
                { text: "Score", value: "score" },
                { text: "Milestones Completed", value: "milestones_completed" },
                { text: "Milestones Missed", value: "milestones_missed" }
            ];


            for (let team of this.teams) {
                this.dashboard_data_items.push({
                    "team_id": team.team_id,
                    "team_name": team.team_name,
                    "team_url": "/team/" + team.team_id,
                    "commits": team.commits,
                    "score": team.score,
                    "total_score": team.total_score,
                    "milestones_completed": team.milestones_completed,
                    "milestones_missed": team.milestones_missed
                });
            }

        }
    },
    mounted() {
        this.create_dashboard();

        
    },
}

</script>

<style scoped>
.milestone-table {
    font-size: 0.75rem;
}

a {
    text-decoration: none;
}
</style>