import { mainAxios } from '@/helpers/ApiHelpers'

export async function createMilestone(milestoneData) {
    try {
        const response = await mainAxios.post('/milestones', JSON.stringify(milestoneData));
        return response.data;
    } catch (error) {
        console.warn("Error creating milestone:", error);
        throw error;
    }
}

export async function fetchMilestones() {
    try {
        const response = await mainAxios.get('/milestones');
        return response.data;
    } catch (error) {
        console.warn("Error fetching milestones:", error);
        throw error;
    }
}

export async function updateMilestone(milestoneId, milestoneData) {
    try {
        const response = await mainAxios.put(`/milestones/${milestoneId}`, JSON.stringify(milestoneData));
        return response.data;
    } catch (error) {
        console.warn("Error updating milestone:", error);
        throw error;
    }
}

export async function deleteMilestone(milestoneId) {
    try {
        const response = await mainAxios.delete(`/milestones/${milestoneId}`);
        return response.data;
    } catch (error) {
        console.warn("Error deleting milestone:", error);
        throw error;
    }
}
