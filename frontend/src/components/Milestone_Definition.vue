<template>
  <div class="define-milestones">
    <!-- Header Section -->
    <header class="header">
      <div class="logo">App Logo</div>
      <div class="user-info">
        <span>Welcome XXX! You are signed in as TA/Instructor.</span>
        <a href="#" class="logout">Logout</a>
      </div>
    </header>

    <!-- Navigation Section -->
    <nav class="navigation">
      <router-link to="/home" class="nav-button">Home</router-link>
      <router-link to="/dashboard" class="nav-button">Dashboard</router-link>
      <router-link to="/define-milestones" class="nav-button active">Define Milestones</router-link>
      <router-link to="/project-scoring" class="nav-button">Project Scoring</router-link>
    </nav>

    <!-- Main Content Section -->
    <main class="content">
<<<<<<< HEAD
      <!-- Button to Open Modal for Creating a Milestone -->
      <b-button @click="modal = true" class="create-btn">Create Milestone</b-button>
=======
      <form class="milestone-form" @submit.prevent="handleSubmit">
        <div class="form-group">
          <label for="milestone-name">Milestone Name</label>
          <input v-model="newMilestone.name" id="milestone-name" type="text" placeholder="Type a new milestone to create or select existing milestone to edit or delete" required />
        </div>

        <div class="form-group">
          <label for="milestone-description">Milestone Description (Max 50 char)</label>
          <textarea v-model="newMilestone.description" id="milestone-description" placeholder="List the tasks which will form part of this milestone" maxlength="50" required></textarea>
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
          <button type="submit" class="submit-btn">Submit</button>
          <button type="button" class="delete-btn" @click="confirmDelete">Delete</button>
          <button type="button" class="cancel-btn" @click="resetForm">Cancel</button>
        </div>
      </form>
>>>>>>> origin/main

      <!-- Dynamic Table for Created Milestones -->
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

    <!-- Modal for Creating a New Milestone -->
    <b-modal v-model="modal" title="Create or Edit Milestone">
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
// Importing necessary components from bootstrap-vue-next
import { ref } from 'vue';
import { BButton, BModal } from 'bootstrap-vue-next';

export default {
  name: 'DefineMilestones',
  components: {
    BButton,
    BModal
  },
  data() {
    return {
      modal: ref(false), // Controls the modal visibility
      newMilestone: {
        name: '',
        description: '',
        startDate: '',
        deadline: '',
        maxMarks: '',
      },
      milestones: [], // Stores created milestones
      editingIndex: null, // Index of the milestone being edited
    };
  },
  methods: {
    handleSubmit() {
      if (this.editingIndex !== null) {
        // Update the existing milestone
        this.milestones[this.editingIndex] = { ...this.newMilestone };
        this.editingIndex = null; // Reset editing state
      } else {
        // Add a new milestone
        this.milestones.push({ ...this.newMilestone });
      }
      this.resetForm();  // Reset form after submission
      this.modal = false; // Close modal after submitting
    },
    editMilestone(index) {
      // Populate the form with the selected milestone's data for editing
      this.newMilestone = { ...this.milestones[index] };
      this.editingIndex = index; // Set the editingIndex to the selected milestone's index
      this.modal = true; // Open the modal
    },
    deleteMilestone(index) {
      if (confirm('Are you sure you want to delete this milestone?')) {
        this.milestones.splice(index, 1);
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
};
</script>

<style scoped>
/* Header styles */
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

/* Navigation styles */
.navigation {
  display: flex;
  gap: 10px;
  padding: 10px;
}

.nav-button {
  padding: 5px 10px;
  background-color: #4d4d4d;
  color: white;
  text-decoration: none;
  border-radius: 5px;
}

.nav-button.active {
  background-color: #bfa060;
}

/* Content area styles */
.content {
  padding: 20px;
}

/* Button styles */
.create-btn {
  background-color: #4d4d4d;
  color: white;
  padding: 10px 15px;
  border-radius: 5px;
}

/* Milestone form styles */
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

/* Styles for the dynamic table */
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