import { mainAxios } from '@/helpers/ApiHelpers'
import TaTeamsDashboardData from './TaTeamsDashboardData.json' assert { type: 'json' }
import TaTeamDashboardData from './TaTeamDashboardData.json' assert { type: 'json' }


export class TaTeamsDashboardApiHelpers{

    static async fetchTeamsData(){
        try {
            const response = await mainAxios.get('/ta-teams');
            console.log("Teams:", response.data)

            const data = typeof response.data === 'string' 
            ? JSON.parse(response.data) 
            : response.data;

        if (!data || !data.teams || !data.milestones) {
            console.warn('Invalid API response format');
            return { teams: TaTeamsDashboardData.teams, milestones: TaTeamsDashboardData.milestones };
        }

            console.log("Teams data:", data)
            return { data: data };
            // return response.data
        } catch (error) {
            console.warn('Using local team data due to error:', error)
            return { teams: TaTeamsDashboardData.teams, milestones: TaTeamsDashboardData.milestones };
        }
    }

    static async fetchTeamData(team_id){
        try {
            const response = await mainAxios.get('/ta-teams'+team_id);
            console.log("Teams:", response.data)

            const data = typeof response.data === 'string' 
            ? JSON.parse(response.data) 
            : response.data;

        if (!data || !data.team || data.members || !data.milestones) {
            console.warn('Invalid API response format');
            return { data: TaTeamDashboardData };
        }

            console.log("Teams data:", data)
            return { data: data };
            // return response.data
        } catch (error) {
            console.warn('Using local team data due to error:', error)
            return { data: TaTeamDashboardData };
        }
    }
}