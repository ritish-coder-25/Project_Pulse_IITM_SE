<template>
  <div class="define-milestones">
    <!-- Rest of the template remains exactly the same -->
    <main class="content" v-if="activeTab === 2">
      <b-button @click="modal = true" class="create-btn">Create Milestone</b-button>

      <table class="milestone-table" v-if="!loading && Array.isArray(milestones) && milestones.length">
        <thead>
          <tr>
            <th>Name</th>
            <th>Description</th>
            <th>Start Date</th>
            <th>End Date</th>
            <th>Max Marks</th>
            <th>Actions</th>
          </tr>
        </thead>
        <tbody>
          <tr v-for="(milestone, index) in milestones" :key="milestone.milestone_id">
            <td>{{ milestone.milestone_name }}</td>
            <td>{{ milestone.milestone_description }}</td>
            <td>{{ milestone.start_date }}</td>
            <td>{{ milestone.end_date }}</td>
            <td>{{ milestone.max_marks }}</td>
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
          <input v-model="formData.milestone_name" id="milestone-name" type="text" placeholder="Enter milestone name" required />
        </div>

        <div class="form-group">
          <label for="milestone-description">Milestone Description (Max 50 characters)</label>
          <textarea v-model="formData.milestone_description" id="milestone-description" placeholder="Describe the tasks for this milestone" maxlength="50" required></textarea>
        </div>

        <div class="form-group">
          <label for="start-date">Milestone Start Date</label>
          <input v-model="formData.start_date" id="start-date" type="date" required />
        </div>

        <div class="form-group">
          <label for="submission-deadline">Submission Deadline</label>
          <input v-model="formData.end_date" id="submission-deadline" type="date" required />
        </div>

        <div class="form-group">
          <label for="max-marks">Max Marks</label>
          <input v-model="formData.max_marks" id="max-marks" type="number" required />
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
        milestone_name: '',
        milestone_description: '',
        start_date: '',
        end_date: '',
        max_marks: '',
        project_id: 1,
      },
      updateMilestone: {
        milestone_name: '',
        milestone_description: '',
        start_date: '',
        end_date: '',
        max_marks: '',
      },
      milestones: [],
      editingIndex: null,
    };
  },
  computed: {
    // Dynamically bind the correct form data based on whether we're editing or creating
    formData() {
      return this.editingIndex !== null ? this.updateMilestone : this.newMilestone;
    }
  },
  methods: {
    resetForm() {
      this.newMilestone = {
        milestone_name: '',
        milestone_description: '',
        start_date: '',
        end_date: '',
        max_marks: '',
        project_id: 1,
      };
      this.updateMilestone = {
        milestone_name: '',
        milestone_description: '',
        start_date: '',
        end_date: '',
        max_marks: '',
      };
      this.editingIndex = null;
    },

    async fetchMilestonesData() {
      try {
        this.loading = true;
        const milestones = await fetchMilestones();
        this.milestones = JSON.parse(milestones) || [];
      } catch (error) {
        console.error('Error fetching milestones:', error);
        this.milestones = [];
      } finally {
        this.loading = false;
      }
    },

    async handleSubmit() {
      try {
        let milestoneData = this.editingIndex !== null ? { ...this.updateMilestone } : { ...this.newMilestone };

        // Ensure dates are in the correct format (YYYY-MM-DD)
        if (milestoneData.start_date && milestoneData.end_date) {
          milestoneData.start_date = new Date(milestoneData.start_date).toISOString().split('T')[0]; // Format to YYYY-MM-DD
          milestoneData.end_date = new Date(milestoneData.end_date).toISOString().split('T')[0]; // Format to YYYY-MM-DD
        }

        // Log the final data to be sent to the API
        console.log("Data to be sent to API:", milestoneData);
        if (this.editingIndex !== null) {
          const id = this.milestones[this.editingIndex].milestone_id;
          if (!id) {
            console.error("No valid milestone ID to update.");
          }
          // Remove unnecessary fields (like milestone_id and project_id)
          delete milestoneData.milestone_id; // For update, avoid sending milestone_id
          delete milestoneData.project_id; // For both new and update, avoid sending project_id
          await updateMilestone(id, milestoneData);
        } else {
          await createMilestone(milestoneData);
        }
        //this.fetchMilestonesData();
        this.resetForm();
        this.modal = false;
      } catch (error) {
        console.error("Error submitting milestone:", error);
      }
    },

    editMilestone(index) {
      this.editingIndex = index;
      this.updateMilestone = { ...this.milestones[index] };
      this.modal = true;
      //this.fetchMilestonesData();
    },

    async deleteMilestone(index) {
      try {
        const id = this.milestones[index].milestone_id;
        await deleteMilestone(id);
        this.milestones.splice(index, 1);
        //this.fetchMilestonesData();
      } catch (error) {
        console.error("Error deleting milestone:", error);
      }
    },
  },
  mounted() {
    this.fetchMilestonesData(); // Fetch milestones when the component is mounted
    console.log('Condition result in mounted:', !this.loading && Array.isArray(this.milestones) && this.milestones.length);
  },
  watch: {
    milestones(newMilestones) {
      console.log('Milestones updated:', newMilestones);
    }
  },
};

//     async mounted() {
//       try {
//         const fetchedMilestones = await fetchMilestones();
//         this.milestones = fetchedMilestones;
//       } catch (error) {
//         console.error("Error fetching milestones:", error);
//       }
//     },

//     resetForm() {
//       this.newMilestone = {
//         name: '',
//         description: '',
//         startDate: '',
//         deadline: '',
//         maxMarks: '',
//       };
//     },
//   },

//   mounted() {
//     this.mounted();
//   },

//   watch: {
//     // Update active tab when route changes externally
//     '$route'(to) {
//       const routeToTabIndex = {
//         '/home': 0,
//         '/dashboard': 1,
//         '/milestone-definition': 2,
//         '/scoring': 3
//       };
//       this.activeTab = routeToTabIndex[to.path] || 2;
//     }
//   }
// };
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