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

export async function fetchProject() {
    try {

        const response = await mainAxios.get('/projects');
        return response.data;

    } catch (error) {
        console.warn("Error fetching project:", error);
        throw error;
    }
};