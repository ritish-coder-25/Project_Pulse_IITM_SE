<template>
  <div class="milestone-info" v-if="milestone">
    <h2>DEADLINES:</h2>
    <ul v-if="milestone.deadlines.length > 0">
      <li v-for="(deadline, index) in milestone.deadlines" :key="index">
        {{ deadline.name }}: <strong>{{ deadline.date }}</strong>
      </li>
    </ul>
    <p v-else>No deadlines available for this milestone.</p>

    <h2>Project Statement:</h2>
    <p class="project-title">{{ milestone.projectTitle }}</p>
    <p class="project-description">{{ milestone.projectDescription }}</p>
  </div>

  <div v-else class="no-milestone">
    <p>No milestone data available.</p>
  </div>
</template>

<script>
import axios from 'axios';

export default {
  name: "MilestoneInfo",
  data() {
    return {
      milestone: null, // Will hold the fetched milestone data
    };
  },
  computed: {
    milestoneId() {
      return this.$route.params.id; // Assuming you pass the milestone ID in the route
    },
  },
  created() {
    this.fetchMilestoneInfo();
  },
  methods: {
    async fetchMilestoneInfo() {
      try {
        const response = await axios.get(`/api/milestones/${this.milestoneId}`, {
          headers: { Authorization: `Bearer ${localStorage.getItem('token')}` }
        });
        this.milestone = response.data;
      } catch (error) {
        console.error("Error fetching milestone data:", error);
        this.milestone = null;
      }
    },
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

.no-milestone {
  font-family: "Arial", sans-serif;
  color: #333;
  background-color: #f9f9fb;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 24px;
  max-width: 600px;
  margin: 0 auto;
  text-align: center;
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.05);
}

.no-milestone p {
  font-size: 18px;
  color: #e74c3c;
  font-weight: bold;
}
</style>
