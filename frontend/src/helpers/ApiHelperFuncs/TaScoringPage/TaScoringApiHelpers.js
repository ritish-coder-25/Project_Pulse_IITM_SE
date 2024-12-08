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

    static async fetchCommits(startDate, endDate) {
        try {
            const response = await mainAxios.post('/commitslist',JSON.stringify({ start_date: startDate, end_date: endDate }));
              
            
            console.log("Commits Response:", response.data);
            // console.log("Commits Response:", typeof(response.data));
    
            // Ensure the response is an array of commits
            if (!Array.isArray(JSON.parse(response.data))) {
                console.warn('Invalid API response format: Expected an array of commits.');
                return { data: TaScoringApiHelpersJson.localCommits }; // Fallback to local data
            }
    
            // Map over the commits to structure data as required
            const commitsArray = JSON.parse(response.data).map(commit => ({
                commit_id: commit.commit_id,
                commit_hash: commit.commit_hash,
                commit_message: commit.commit_message,
                commit_score: commit.commit_score,
                commit_clarity: commit.commit_clarity,
                complexity_score: commit.complexity_score,
                code_quality_score: commit.code_quality_score,
                improvement_suggestions: commit.improvement_suggestions || [],
                commit_date: commit.commit_timestamp,
                observations: commit.additional_observations,
                risk_assessment: commit.risk_assessment,
                commit_changes: commit.commit_changes,
                analysis_timestamp: commit.analysis_timestamp,
                user_id: commit.user_id,


            //     'commit_id': self.commit_id,
            // 'user_id': self.user_id,
            // 'team_id': self.team_id,
            // 'commit_hash': self.commit_hash,
            // 'commit_message': self.commit_message,
            // 'commit_timestamp': self.commit_timestamp,
            // 'commit_score': self.commit_score,
            // 'commit_changes': self.commit_changes,
            // 'commit_clarity': self.commit_clarity,
            // 'complexity_score': self.complexity_score,
            // 'code_quality_score': self.code_quality_score,
            // 'risk_assessment': self.risk_assessment,
            // 'improvement_suggestions': self.improvement_suggestions,
            // 'analysis_timestamp': self.analysis_timestamp,
            // 'additional_observations': self.additional_observations,
            }));
    
            console.log("Processed Commits Array:", commitsArray);
            return { data: commitsArray };
        } catch (error) {
            console.warn('Using local commits data due to error:', error);
            return { data: TaScoringApiHelpersJson.localCommits }; // Fallback to local data
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

    static async startCeleryTask(teamId, startTime, endTime) {
        try {
            // Sending POST request to trigger the Celery task
            const payload = {
                team_id: teamId.teamId,
                start_time: teamId.startTime,
                end_time: teamId.endTime
            }

            console.log("Celery task payload:", payload);

            const response = await mainAxios.post('/celery-test', JSON.stringify(payload));
               

            console.log("Celery task started:", response.data);
            return JSON.parse(response.data); // Return the task ID and message
        } catch (error) {
            console.warn('Error triggering Celery task:', error);
            throw error;
        }
    }

    // Function to fetch the task status
    static async getTaskStatus(taskId) {
        try {
            // Sending GET request to fetch the task status
            const response = await mainAxios.get(`/task_status/${taskId}`);
            
            console.log("Task status:", response.data);
            return response.data; // Return the task status info
        } catch (error) {
            console.warn('Error fetching task status:', error);
            throw error;
        }
    }

}
