import { mainAxios } from '@/helpers/ApiHelpers'
import TaTeamsDashboardData from './TaTeamsDashboardData.json' assert { type: 'json' }
import TaTeamDashboardData from './TaTeamDashboardData.json' assert { type: 'json' }


export class TaTeamsDashboardApiHelpers{

    static async fetchTeamsData(){
        try {
            const response = await mainAxios.get('/ta-teams', {timeout: 2000});
            // console.log("Teams:", response.data)

            const data = typeof response.data === 'string' 
            ? JSON.parse(response.data) 
            : response.data;

        if (!data || !data.teams || !data.milestones) {
            console.warn('Invalid API response format');
            return null
        }
        
        // console.log("Teams data:", data)
        return { data: data };
        } catch (error) {
            console.warn('Error while fetching teams data:', error)
            return null
        }
    }

    static async fetchTeamData(team_id){
        try {
            const response = await mainAxios.get('/ta-teams/'+team_id, {timeout: 2000});
            // console.log("Teams:", response.data)

            const data = typeof response.data === 'string' 
            ? JSON.parse(response.data) 
            : response.data;

        if (!data || !data.team || !data.members || !data.milestones) {
            console.warn('Invalid API response format');
            return null
        }

            // console.log("Teams data:", data)
            return { data: data };
        } catch (error) {
            console.error('Error while fetching team data:', error)
            return null
        }
    }
}