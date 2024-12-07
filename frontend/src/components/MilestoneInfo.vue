<template>
  <div class="milestone-info">
    <h2>DEADLINES:</h2>
    <ul>
      <li>Milestone 1 and Milestone 2: Deadline by the end of Week 4: <strong>20th October</strong></li>
      <li>Milestone 3: Deadline by the end of Week 6: <strong>10th November</strong></li>
      <li>Milestone 4: Deadline by the end of Week 8: <strong>17th November</strong></li>
      <li>Milestone 5: Deadline by the end of Week 10: <strong>27th November</strong></li>
      <li>Milestone 6: Deadline by the end of Week 11: <strong>8th December</strong></li>
    </ul>

    <h2>Project Statement:</h2>
    <p class="project-title">Tracking Student Progress in Software Projects</p>
    <p class="project-description">
      In course projects such as the ones you have already done in Application Development I and II,
      it can be challenging for instructors to effectively track the progress of student projects,
      particularly in larger classes where multiple teams are working on different tasks...
    </p>

    <h2>Project Docuemnt</h2>
    <p>Project Document Link: <a :href="project_document_url" target="_blank">{{ project_document_url }}</a></p>
  </div>
</template>

<script>
import moment from 'moment';
import { getProjectDetails } from '@/helpers/ApiHelperFuncs/ProjectDetails';

export default {
  name: "MilestoneInfo",

  data(){
    return {
      project_id: null,
      project_topic: "",
      project_statement: "",
      project_document_url: "",
      fetchDataError:false
    }
  },
  methods:{
    async fetchProjectDetails(){
      const data = await getProjectDetails();
      if(data){
            this.project_id = data.project_id,
            this.project_topic = data.project_topic,
            this.project_statement = data.statement,
            this.project_document_url = data.document_url
        }else{
            console.error("Error while fetching teams dashboard data!!")
            this.fetchDataError = true
        }
    }
  },
  mounted(){
    this.fetchProjectDetails()
  },
};
</script>

<style scoped>
.milestone-info {
  font-family: "Arial", sans-serif;
  color: #333;
  background-color: #f9f9fb;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 24px;
  max-width: 600px;
  margin: 0 auto;
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.05);
}

h2 {
  font-size: 20px;
  font-weight: 600;
  color: #2c3e50;
  border-bottom: 2px solid #e0e0e0;
  padding-bottom: 8px;
  margin-top: 24px;
  margin-bottom: 16px;
}

ul {
  list-style-type: none;
  padding-left: 0;
  margin-bottom: 24px;
}

ul li {
  font-size: 16px;
  line-height: 1.8;
  color: #34495e;
  padding: 8px 0;
  border-left: 4px solid #3498db;
  padding-left: 12px;
  margin-bottom: 8px;
  background-color: #eef7fd;
  border-radius: 4px;
}

ul li strong {
  color: #e74c3c;
}

.project-title {
  font-weight: bold;
  font-size: 18px;
  color: #2c3e50;
  margin-top: 20px;
  margin-bottom: 10px;
}

.project-description {
  font-size: 16px;
  line-height: 1.6;
  color: #555;
  background-color: #fafafa;
  padding: 16px;
  border-left: 4px solid #3498db;
  border-radius: 4px;
  box-shadow: inset 0px 1px 2px rgba(0, 0, 0, 0.05);
}

a{
  text-decoration: none;
}
</style>
