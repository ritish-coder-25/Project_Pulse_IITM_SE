<template>
  <div class="define-milestones">
    <!-- Rest of the template remains exactly the same -->
    <main class="content" v-if="activeTab === 2">
      <b-button @click="modal = true" class="create-btn">Create Milestone</b-button>

      <table class="milestone-table" v-if="milestones.length">
        <thead>
          <tr>
            <th>Name</th>
            <th>Description</th>
            <th>Start Date</th>
            <th>Deadline</th>
            <th>Max Marks</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(milestone, index) in milestones" :key="index">
            <td>{{ milestone.name }}</td>
            <td>{{ milestone.description }}</td>
            <td>{{ milestone.startDate }}</td>
            <td>{{ milestone.deadline }}</td>
            <td>{{ milestone.maxMarks }}</td>
            <td>
              <button @click="editMilestone(index)" class="edit-btn">Edit</button>
              <button @click="deleteMilestone(index)" class="delete-btn">Delete</button>
            </td>
          </tr>
        </tbody>
      </table>
    </main>

    <!-- Updated Modal with hide-footer prop -->
    <b-modal v-model="modal" title="Create or Edit Milestone" hide-footer>
      <form class="milestone-form" @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="milestone-name">Milestone Name</label>
          <input v-model="newMilestone.name" id="milestone-name" type="text" placeholder="Enter milestone name" required />
        </div>

        <div class="form-group">
          <label for="milestone-description">Milestone Description (Max 50 characters)</label>
          <textarea v-model="newMilestone.description" id="milestone-description" placeholder="Describe the tasks for this milestone" maxlength="50" required></textarea>
        </div>

        <div class="form-group">
          <label for="start-date">Milestone Start Date</label>
          <input v-model="newMilestone.startDate" id="start-date" type="date" required />
        </div>

        <div class="form-group">
          <label for="submission-deadline">Submission Deadline</label>
          <input v-model="newMilestone.deadline" id="submission-deadline" type="date" required />
        </div>

        <div class="form-group">
          <label for="max-marks">Max Marks</label>
          <input v-model="newMilestone.maxMarks" id="max-marks" type="number" required />
        </div>

        <div class="form-actions">
          <button type="submit" class="submit-btn">{{ editingIndex !== null ? 'Update' : 'Submit' }}</button>
          <button type="button" class="cancel-btn" @click="modal = false">Cancel</button>
        </div>
      </form>
    </b-modal>
  </div>
</template>

<script>
import { ref } from 'vue';
import { useRouter, useRoute } from 'vue-router';
import { BButton, BModal, BTabs, BTab } from 'bootstrap-vue-next';
import { 
  Home, 
  LayoutDashboard, 
  ClipboardCheck, 
  Flag as Milestone 
} from 'lucide-vue-next';

import { createMilestone, updateMilestone, deleteMilestone, fetchMilestones } from '@/helpers/ApiHelperFuncs/MilestoneDefinition/MilestoneDefinitionApiHelpers';

export default {
  name: 'DefineMilestones',
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
    
    // Map routes to tab indices
    const routeToTabIndex = {
      '/home': 0,
      '/dashboard': 1,
      '/milestone-definition': 2,
      '/scoring': 3
    };

    // Map tab indices to routes
    const tabIndexToRoute = {
      0: '/home',
      1: '/dashboard',
      2: '/milestone-definition',
      3: '/scoring'
    };

    // Set initial active tab based on current route
    const initialTab = routeToTabIndex[route.path] || 2;

    return {
      router,
      route,
      tabIndexToRoute,
      initialTab
    };
  },
  data() {
    return {
      modal: ref(false),
      activeTab: this.initialTab,
      newMilestone: {
        name: '',
        description: '',
        startDate: '',
        deadline: '',
        maxMarks: '',
      },
      milestones: [],
      editingIndex: null,
    };
  },
  methods: {
    handleTabChange(newIndex) {
      const targetRoute = this.tabIndexToRoute[newIndex];
      if (targetRoute && this.route.path !== targetRoute) {
        this.router.push(targetRoute);
      }
    },
    async handleSubmit() {
      try {
        const milestoneData = {
          milestone_name: this.newMilestone.name,
          milestone_description: this.newMilestone.description,
          start_date: this.newMilestone.startDate,
          end_date: this.newMilestone.deadline,
          max_marks: this.newMilestone.maxMarks,
          project_id: 1,
        };

        if (this.editingIndex !== null) {
          const updatedMilestone = await updateMilestone(this.milestones[this.editingIndex].id, milestoneData);
          this.milestones[this.editingIndex] = updatedMilestone;
          this.editingIndex = null;
        } else {
          const createdMilestone = await createMilestone(milestoneData);
          this.milestones.push(createdMilestone);
        }

        this.resetForm();
        this.modal = false;
      } catch (error) {
        console.error("Error handling milestone:", error);
      }
    },

    editMilestone(index) {
      this.newMilestone = { ...this.milestones[index] };
      this.editingIndex = index;
      this.modal = true;
    },

    async deleteMilestone(index) {
      try {
        const milestoneId = this.milestones[index].id;
        await deleteMilestone(milestoneId);
        this.milestones.splice(index, 1);
      } catch (error) {
        console.error("Error deleting milestone:", error);
      }
    },

    async mounted() {
      try {
        const fetchedMilestones = await fetchMilestones();
        this.milestones = fetchedMilestones;
      } catch (error) {
        console.error("Error fetching milestones:", error);
      }
    },

    resetForm() {
      this.newMilestone = {
        name: '',
        description: '',
        startDate: '',
        deadline: '',
        maxMarks: '',
      };
    },
  },

  mounted() {
    this.mounted();
  },

  watch: {
    // Update active tab when route changes externally
    '$route'(to) {
      const routeToTabIndex = {
        '/home': 0,
        '/dashboard': 1,
        '/milestone-definition': 2,
        '/scoring': 3
      };
      this.activeTab = routeToTabIndex[to.path] || 2;
    }
  }
};
</script>

<style scoped>
/* All styles remain exactly the same */
.header {
  display: flex;
  justify-content: space-between;
  background-color: #6b6b6b;
  color: white;
  padding: 10px;
}

.logo {
  font-size: 1.2em;
}

.user-info {
  display: flex;
  align-items: center;
}

.logout {
  margin-left: 10px;
  color: white;
  text-decoration: none;
}

.custom-tabs {
  padding: 10px;
}

.tab-title {
  display: flex;
  align-items: center;
  gap: 8px;
  cursor: pointer;
}

.tab-icon {
  width: 20px;
  height: 20px;
}

.content {
  padding: 20px;
}

/* Rest of the styles remain the same */
.create-btn {
  background-color: #4d4d4d;
  color: white;
  padding: 10px 15px;
  border-radius: 5px;
}

.milestone-form {
  display: flex;
  flex-direction: column;
}

.form-group {
  margin-bottom: 15px;
}

.form-group label {
  font-weight: bold;
}

.form-group input,
.form-group textarea {
  width: 100%;
  padding: 5px;
  border: 1px solid #ccc;
  border-radius: 4px;
}

.form-actions {
  display: flex;
  gap: 10px;
}

.submit-btn,
.delete-btn,
.cancel-btn {
  padding: 5px 15px;
  background-color: #4d4d4d;
  color: white;
  border: none;
  border-radius: 5px;
  cursor: pointer;
}

.delete-btn {
  background-color: #ff4d4d;
}

.cancel-btn {
  background-color: #a5a5a5;
}

.milestone-table {
  width: 100%;
  border-collapse: collapse;
  margin-top: 20px;
}

.milestone-table th,
.milestone-table td {
  padding: 10px;
  border: 1px solid #ddd;
  text-align: center;
}

.milestone-table th {
  background-color: #4d4d4d;
  color: white;
}

.milestone-table td .delete-btn {
  padding: 5px 10px;
  background-color: #ff4d4d;
  color: white;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}

.milestone-table td .edit-btn {
  padding: 5px 10px;
  background-color: #ffbb33;
  color: white;
  border: none;
  border-radius: 3px;
  cursor: pointer;
}
</style>