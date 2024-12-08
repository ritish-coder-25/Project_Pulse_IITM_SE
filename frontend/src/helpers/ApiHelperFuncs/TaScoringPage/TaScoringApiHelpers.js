import { mainAxios } from '@/helpers/ApiHelpers'
import TaScoringApiHelpersJson from './TaScoringApiHelpers.json' assert { type: 'json' }
import { UserRoleEnums } from '@/enums'

export class TaScoringApiHelpers {

    static async fetchTeams() {
        try {
            const response = await mainAxios.get('/teams/all');
            console.log("Teams:", response.data);

            const data = typeof response.data === 'string'
                ? JSON.parse(response.data)
                : response.data;

            // Ensure the response has a valid format
            if (!data || !data.teams || !Array.isArray(data.teams)) {
                console.warn('Invalid API response format');
                return { data: TaScoringApiHelpersJson.localTeams };
            }

            // Map over the teams array to extract required fields
            const teamsArray = data.teams.map(team => ({
                id: team.team_id,
                name: team.team_name
            }));

            console.log("Teams array:", teamsArray);
            return { data: teamsArray };
        } catch (error) {
            console.warn('Using local team data due to error:', error);
            return { data: TaScoringApiHelpersJson.localTeams };
        }
    }


    static async fetchMilestones() {
        try {
            const response = await mainAxios.get('/milestones')

            const data = typeof response.data === 'string'
                ? JSON.parse(response.data)
                : response.data;

            if (!data) {
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
            const response = await mainAxios.get(`/uploaded-files2/${teamId}`);

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
                milestone: doc.milestoneId
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
    static async submitMilestoneReview(payload) {
        try {
            // Ensure payload is a valid JSON object
            const jsonPayload = JSON.stringify(payload); // Convert payload to JSON string

            const response = await mainAxios.post('/milestone-review', jsonPayload);

            const data = typeof response.data === 'string'
                ? JSON.parse(response.data)
                : response.data;

            if (!data || !data.message) {
                console.warn('Invalid API response format');
                throw new Error('Invalid API response format');
            }

            console.log("Milestone review response:", data);
            return data; // Assuming data contains the `message`
        } catch (error) {
            console.warn('Fallback to default error handling for milestone review:', error);
            throw error.response?.data || { message: "An unexpected error occurred" };
        }
    }

}
