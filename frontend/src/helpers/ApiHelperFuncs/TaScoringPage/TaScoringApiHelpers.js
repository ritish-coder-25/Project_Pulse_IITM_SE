import { mainAxios } from '@/helpers/ApiHelpers'
import TaScoringApiHelpersJson from './TaScoringApiHelpers.json' assert { type: 'json' }
import { UserRoleEnums } from '@/enums'

export class TaScoringApiHelpers {

    static async fetchTeams() {
        try {
            const response = await mainAxios.get('/teams');
            console.log("Teams:", response.data)

            const data = typeof response.data === 'string' 
            ? JSON.parse(response.data) 
            : response.data;

        if (!data || !data.team) {
            console.warn('Invalid API response format');
            return { data: TaScoringApiHelpersJson.localTeams };
        }

            const teamsArray = [{
                id: data.team.team_id,
                name: data.team.team_name
            }];
            console.log("Teams array:", teamsArray)
            return { data: teamsArray };
            // return response.data
        } catch (error) {
            console.warn('Using local team data due to error:', error)
            return TaScoringApiHelpersJson.localTeams
        }
    }

    static async fetchMilestones() {
        try {
            const response = await mainAxios.get('/milestones')

            const data = typeof response.data === 'string' 
            ? JSON.parse(response.data) 
            : response.data;

        if (!data ) {
            console.warn('Invalid API response format');
            return { data: TaScoringApiHelpersJson.milestones };
        }

            
            console.log("Milestones array:", data)
            return { data: data };
            return response.data
        } catch (error) {
            console.warn('Using local milestone data due to error:', error)
            return TaScoringApiHelpersJson.localMilestones
        }
    }

    static async fetchDocs(teamId) {
        try {
            const response = await mainAxios.get(`/files/${teamId}`);
            
            console.log("Documents:", response.data)
            const data = typeof response.data === 'string' 
                ? JSON.parse(response.data) 
                : response.data;

            if (!data || !data.documents) {
                console.warn('Invalid API response format');
                return { data: TaScoringApiHelpersJson.documents };
            }

            // Map the array of documents directly
            const docsArray = data.documents.map(doc => ({
                id: doc.id,
                name: doc.name,
                url: doc.url,
                team: doc.team,
                milestone: doc.milestone
            }));
            
            console.log("Docs array:", docsArray)
            return { data: docsArray };
        } catch (error) {
            console.warn('Using local document data due to error:', error)
            return TaScoringApiHelpersJson.localDocuments
        }
    }

    static async downloadFile(fileId) {
        const response = await mainAxios.get(`/download/${fileId}`);
        return response;
    }
}
