import { mainAxios } from '@/helpers/ApiHelpers'

import { UserRoleEnums } from '@/enums'


export async function createProject(projectData) {
    try {
        
        const response = await mainAxios.post('/projects', JSON.stringify(projectData));
        return response.data;
        
    } catch (error) {
        console.warn("Error creating project:", error);
        throw error;
    }
};