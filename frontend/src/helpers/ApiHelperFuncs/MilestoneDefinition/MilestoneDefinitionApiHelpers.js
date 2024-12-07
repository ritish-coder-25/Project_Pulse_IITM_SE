import { mainAxios } from '@/helpers/ApiHelpers';

/**
 * Create a new milestone.
 * 
 * @param {Object} milestoneData - The data for the milestone to be created.
 * @returns {Promise<Object>} - The API response containing the created milestone details.
 */
export async function createMilestone(milestoneData) {
    try {
        const response = await mainAxios.post('/api/milestones', JSON.stringify(milestoneData));
        return response.data;
    } catch (error) {
        console.warn("Error creating milestone:", error);
        throw error;
    }
}

/**
 * Update an existing milestone.
 * 
 * @param {number} milestoneId - The ID of the milestone to be updated.
 * @param {Object} milestoneData - The updated data for the milestone.
 * @returns {Promise<Object>} - The API response containing the updated milestone details.
 */
export async function updateMilestone(milestoneId, milestoneData) {
    try {
        const response = await mainAxios.put(`/api/milestones/${milestoneId}`, JSON.stringify(milestoneData));
        return response.data;
    } catch (error) {
        console.warn("Error updating milestone:", error);
        throw error;
    }
}

/**
 * Delete an existing milestone.
 * 
 * @param {number} milestoneId - The ID of the milestone to be deleted.
 * @returns {Promise<Object>} - The API response confirming the deletion.
 */
export async function deleteMilestone(milestoneId) {
    try {
        const response = await mainAxios.delete(`/api/milestones/${milestoneId}`);
        return response.data;
    } catch (error) {
        console.warn("Error deleting milestone:", error);
        throw error;
    }
}

/**
 * Fetch all milestones.
 * 
 * @returns {Promise<Object[]>} - The API response containing a list of milestones.
 */
export async function fetchMilestones() {
    try {
        const response = await mainAxios.get('/api/milestones');
        return response.data;
    } catch (error) {
        console.warn("Error fetching milestones:", error);
        throw error;
    }
}
