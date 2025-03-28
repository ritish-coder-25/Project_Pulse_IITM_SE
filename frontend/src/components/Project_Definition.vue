<template>
  <div class="container">
    <!-- Project Definition Form -->
    <div class="form-container">
      <form @submit.prevent="handleSubmit">
        <!-- Project Name -->
        <label for="project-name">Project Name</label>
        <input id="project-name" type="text" v-model="name" required />

        <!-- Project Statement -->
        <label for="project-statement">Project Statement</label>
        <textarea id="project-statement" v-model="statement" placeholder="(List the tasks which will form part of this milestone)" required></textarea>

        <!-- Project Document URL -->
        <label for="project-url">Project Document URL</label>
        <input id="project-url" type="text" v-model="document_url" required />

        <!-- Buttons -->
        <div class="form-buttons">
          <button type="submit" class="submit-button">Submit</button>
          <button type="button" class="cancel-button" @click="handleCancel">Cancel</button>
        </div>
      </form>
    </div>
  </div>
</template>

<script>
import { ref, onMounted } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { BButton, BModal, BTabs, BTab } from 'bootstrap-vue-next';
import { Home, LayoutDashboard, ClipboardCheck, Milestone } from 'lucide-vue-next';
import axios from 'axios';
import { createProject } from '@/helpers/ApiHelperFuncs/ProjectDefinition';
import { fetchProject } from '@/helpers/ApiHelperFuncs/ProjectDefinition';

export default {
  name: 'DefineProject',
  components: {
    BButton,
    BModal,
    BTabs,
    BTab,
    Home,
    LayoutDashboard,
    Milestone,
    ClipboardCheck
  },
  setup() {
    const router = useRouter();
    const route = useRoute();
    const activeTab = ref(0);

    // Map routes to tab indices
    const routeToTabIndex = {
      '/home': 0,
      '/dashboard': 1,
      '/project-definition': 2,
      '/scoring': 3
    };

    // Map tab indices to routes
    const tabIndexToRoute = {
      0: '/home',
      1: '/dashboard',
      2: '/project-definition',
      3: '/scoring'
    };

    // Handler for tab changes
    const handleTabChange = (tabIndex) => {
      router.push(tabIndexToRoute[tabIndex]);
    };

    // Set initial active tab based on current route
    activeTab.value = routeToTabIndex[route.path] || 2;

    return {
      activeTab,
      handleTabChange
    };
  },
  data() {
    return {
      name: '',
      statement: '',
      document_url: '',
    };
  },
  methods: {
    async fetchProjectDetails() {
      this.loading = true;
      this.error = '';

      try {
        const project = await fetchProject()
        const parsedProject = JSON.parse(project)
        console.log(project, typeof project, parsedProject.name,parsedProject.statement,parsedProject.document_url);
        this.name = parsedProject.name;
        this.statement = parsedProject.statement;
        this.document_url = parsedProject.document_url;
      } catch (error) {
        console.error('Error fetching project details:', error);
        this.error = 'Failed to fetch project details. Please try again later.';
      } finally {
        this.loading = false;
      }
    },

    async handleSubmit() {
      let projectData = {
        name: this.name,
        statement: this.statement,
        document_url: this.document_url
      };

      try {
        const response = await createProject(projectData);
        alert('Project edited successfully');

      } catch (error) {

        if (error.response) {
          console.log('Error Data: ', error.response.data);
          // The request was made and the server responded with a status code
          const errorDataString = error.response.data;
          const errorData = JSON.parse(errorDataString);

          if (errorData.errors?.json?.document_url) {
            const urlError = errorData.errors.json.document_url[0];
            alert (urlError);
          }
          else {
            alert('Unknown Error occurred. Please try again.');
          }
        }
        else {
          alert('Failed to connect to the server. Please try again.');
        }
      }
    },
    handleCancel() {
      // Cancel form logic here, reset form or navigate away
      this.name = '';
      this.statement = '';
      this.document_url = '';
    },
  },
  mounted() {
    this.fetchProjectDetails()},
};
</script>

<style scoped>
.container {
  width: 80%;
  margin: 0 auto;
  font-family: Arial, sans-serif;
}

/* Header */
.header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #a0a0a0;
  color: #fff;
  padding: 10px 20px;
}

.app-logo {
  font-size: 1.2em;
  font-weight: bold;
}

.user-info {
  font-size: 0.9em;
}

.logout {
  color: #fff;
  text-decoration: underline;
  margin-left: 10px;
}

/* Custom Tabs Styling */
.custom-tabs {
  margin-top: 20px;
}

.tab-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.tab-icon {
  width: 1.2em;
  height: 1.2em;
}

/* Form */
.form-container {
  padding: 20px;
  border: 1px solid #ccc;
  background-color: #f9f9f9;
  margin-top: 20px;
}

label {
  display: block;
  margin: 10px 0 5px;
  font-weight: bold;
}

input[type="text"],
textarea {
  width: 100%;
  padding: 8px;
  margin-bottom: 15px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

textarea {
  resize: vertical;
  height: 60px;
  font-family: Arial, sans-serif;
}

/* Buttons */
.form-buttons {
  display: flex;
  justify-content: flex-end;
  gap: 10px;
}

.submit-button,
.cancel-button {
  padding: 10px 20px;
  font-size: 1em;
  cursor: pointer;
  border: none;
  color: #fff;
}

.submit-button {
  background-color: #888;
}

.cancel-button {
  background-color: #aaa;
}

.submit-button:hover {
  background-color: #666;
}

.cancel-button:hover {
  background-color: #888;
}
</style>