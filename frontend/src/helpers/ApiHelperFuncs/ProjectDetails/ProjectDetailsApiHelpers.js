import { mainAxios } from '@/helpers/ApiHelpers'

export async function getProjectDetails(){
    try {
        
        const response = await mainAxios.get('/stu_home/project');
        
        const data = typeof response.data === 'string' 
            ? JSON.parse(response.data) 
            : response.data;

        return data
        
    } catch (error) {
        console.warn("Error creating project:", error);
        throw error;
    }
};