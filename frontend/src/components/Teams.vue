<template>
    <div class="container mt-4 p-4 border border rounded">
        <h2 class="mb-4">TA/Instructor Dashboard</h2>

        <!-- Teams Table -->
        <h4 class="mb-3">Teams</h4>

        <div class="table border-secondary">
            <EasyDataTable :headers="dashboard_data_headers" :items="dashboard_data_items" :hide-footer=true
                :alternating=true body-text-direction="center" header-text-direction="center"
                table-class-name="customize-table">

                <!-- team name -->
                <template #item-team_name="{ team_name, team_url }">
                    <a :href="team_url">{{ team_name }}</a>
                </template>

                <!-- team score -->
                <template #item-score="{ score, max_score }">
                    {{ score }} / {{ max_score }}
                </template>
            </EasyDataTable>
        </div>


        <!-- Milestone's Table -->
        <h4 class="mb-3">Deadlines</h4>
        <table class="milestone-table table text-center table-bordered table-striped">
            <thead>
                <tr>
                    <th v-for="milestone in milestones">{{ milestone.name }}</th>
                </tr>
            </thead>
            <tbody>
                <tr>
                    <td v-for="milestone in milestones">{{ milestone.end_date }}</td>
                </tr>
            </tbody>
        </table>
    </div>
</template>

<script>

import axios from 'axios';

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
            team_commits: [],
            teamScore: 18,
            maxTeamScore: 20,
            localTeams: [
                { id: 1, name: 'Team A' },
                { id: 2, name: 'Team B' },
                { id: 3, name: 'Team C' },
                { id: 4, name: 'Team D' },
                { id: 5, name: 'Team E' },
            ],
            localTeamCommits: [
                { id: 1, team_id: 1, commits: 80 },
                { id: 2, team_id: 2, commits: 90 },
                { id: 3, team_id: 3, commits: 70 },
                { id: 4, team_id: 4, commits: 65 },
                { id: 5, team_id: 5, commits: 57 },
            ],
            localMilestones: [
                { id: 1, name: 'Milestone 1', description: 'Milestone 1', start_date: '2024-10-10', end_date: '2024-10-20', max_marks: 100 },
                { id: 2, name: 'Milestone 2', description: 'Milestone 2', start_date: '2024-10-10', end_date: '2024-10-20', max_marks: 100 },
                { id: 3, name: 'Milestone 3', description: 'Milestone 3', start_date: '2024-10-20', end_date: '2024-11-10', max_marks: 100 },
                { id: 4, name: 'Milestone 4', description: 'Milestone 4', start_date: '2024-11-02', end_date: '2024-11-17', max_marks: 100 },
                { id: 5, name: 'Milestone 5', description: 'Milestone 5', start_date: '2024-11-15', end_date: '2024-11-27', max_marks: 100 },
                { id: 6, name: 'Milestone 6', description: 'Milestone 6', start_date: '2024-11-22', end_date: '2024-12-08', max_marks: 100 },
            ],
            localMilestoneStatuses: [
                { id: 1, team_id: 1, milestone_id: 1, milestone_status: 'Evaluated', completed_date: '2024-10-20', eval_date: '2024-10-20', eval_score: 90, eval_feedback: 'test msg' },
                { id: 2, team_id: 2, milestone_id: 1, milestone_status: 'Evaluated', completed_date: '2024-10-20', eval_date: '2024-10-20', eval_score: 90, eval_feedback: 'test msg' },
                { id: 3, team_id: 3, milestone_id: 1, milestone_status: 'Missed', completed_date: '', eval_date: '', eval_score: null, eval_feedback: '' },
                { id: 4, team_id: 4, milestone_id: 1, milestone_status: 'Evaluated', completed_date: '2024-10-20', eval_date: '2024-10-20', eval_score: 90, eval_feedback: 'test msg' },
                { id: 5, team_id: 5, milestone_id: 1, milestone_status: 'Evaluated', completed_date: '2024-10-20', eval_date: '2024-10-20', eval_score: 90, eval_feedback: 'test msg' },
                { id: 6, team_id: 1, milestone_id: 2, milestone_status: 'Evaluated', completed_date: '2024-10-20', eval_date: '2024-10-20', eval_score: 90, eval_feedback: 'test msg' },
                { id: 7, team_id: 2, milestone_id: 2, milestone_status: 'Missed', completed_date: '', eval_date: '', eval_score: null, eval_feedback: '' },
                { id: 8, team_id: 3, milestone_id: 2, milestone_status: 'Evaluated', completed_date: '2024-10-20', eval_date: '2024-10-20', eval_score: 90, eval_feedback: 'test msg' },
                { id: 9, team_id: 4, milestone_id: 2, milestone_status: 'Evaluated', completed_date: '2024-10-20', eval_date: '2024-10-20', eval_score: 90, eval_feedback: 'test msg' },
                { id: 10, team_id: 5, milestone_id: 2, milestone_status: 'Evaluated', completed_date: '2024-10-20', eval_date: '2024-10-20', eval_score: 90, eval_feedback: 'test msg' },
                { id: 11, team_id: 1, milestone_id: 3, milestone_status: 'Completed', completed_date: '2024-10-20', eval_date: '', eval_score: null, eval_feedback: '' },
                { id: 12, team_id: 2, milestone_id: 3, milestone_status: 'Pending', completed_date: '', eval_date: '', eval_score: null, eval_feedback: '' },
                { id: 13, team_id: 3, milestone_id: 3, milestone_status: 'Pending', completed_date: '', eval_date: '', eval_score: null, eval_feedback: '' },
                { id: 14, team_id: 4, milestone_id: 3, milestone_status: 'Completed', completed_date: '2024-10-28', eval_date: '', eval_score: null, eval_feedback: '' },
                { id: 15, team_id: 5, milestone_id: 3, milestone_status: 'Pending', completed_date: '', eval_date: '', eval_score: null, eval_feedback: '' },
            ],
        };

    },
    methods: {
        async fetchTeams() {
            try {
                const response = await axios.get('http://localhost:5000/teams');
                this.teams = response.data;
            } catch (error) {
                console.warn("Using local teams data due to error:", error);
                this.teams = this.localTeams;
            }
        },
        async fetchCommits() {
            try {
                const response = await axios.get('http://localhost:5000/commits');
                this.team_commits = response.data;
            } catch (error) {
                console.warn("Using local teams data due to error:", error);
                this.team_commits = this.localTeamCommits;
            }
        },
        async fetchMilestones() {
            try {
                const response = await axios.get('http://localhost:5000/milestones');
                this.milestones = response.data;
            } catch (error) {
                console.warn("Using local milestones data due to error:", error);
                this.milestones = this.localMilestones;
            }
        },
        async fetchMilestoneStatuses() {
            try {
                const response = await axios.get('http://localhost:5000/milestonestatuses');
                this.milestones = response.data;
            } catch (error) {
                console.warn("Using local milestone status data due to error:", error);
                this.milestone_statuses = this.localMilestoneStatuses;
            }
        },
        async create_dashboard_data() {

            await this.fetchTeams();
            await this.fetchCommits();
            await this.fetchMilestones();
            await this.fetchMilestoneStatuses();

            let dashboard_data = {};

            let milestones = {};

            for (let milestone of this.milestones) {
                milestones[milestone.id] = milestone
            }

            for (let team of this.teams) {
                dashboard_data[team.id] = { team_id: team.id, team_name: team['name'], team_url: '/team/' + team.id, commits_count: 0, score: 0, max_score: 0, milestones_completed: 0, milestones_missed: 0 };
            };

            for (let commit of this.team_commits) {
                dashboard_data[commit.team_id]['commits_count'] = commit['commits'];
            };

            for (let status of this.milestone_statuses) {
                if (status['milestone_status'] == "Evaluated") {
                    dashboard_data[status['team_id']]['milestones_completed'] += 1;
                    dashboard_data[status['team_id']]['score'] += status['eval_score'];
                    dashboard_data[status['team_id']]['max_score'] += milestones[status['milestone_id']]['max_marks'];
                } else if (status['milestone_status'] == "Missed") {
                    dashboard_data[status.team_id]['milestones_missed'] += 1;
                    dashboard_data[status['team_id']]['score'] += 0;
                    dashboard_data[status['team_id']]['max_score'] += milestones[status['milestone_id']]['max_marks'];
                }
            };

            console.log(dashboard_data)

            this.dashboard_data_headers = [
                { text: "Team Name", value: "team_name" },
                { text: "No of Commits", value: "commits_count" },
                { text: "Score", value: "score" },
                { text: "Milestones Completed", value: "milestones_completed" },
                { text: "Milestones Missed", value: "milestones_missed" }
            ];

            Object.keys(dashboard_data).forEach(key => {
                this.dashboard_data_items.push(dashboard_data[key]);
            });

        }
    },
    mounted() {
        this.create_dashboard_data();
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