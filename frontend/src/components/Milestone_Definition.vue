``<template>
    <div class="define-milestones">
      <header class="header">
        <div class="logo">App Logo</div>
        <div class="user-info">
          <span>Welcome XXX! You are signed in as TA/Instructor.</span>
          <a href="#" class="logout">Logout</a>
        </div>
      </header>
  
      <nav class="navigation">
        <router-link to="/home" class="nav-button">Home</router-link>
        <router-link to="/dashboard" class="nav-button">Dashboard</router-link>
        <router-link to="/define-milestones" class="nav-button active">Define Milestones</router-link>
        <router-link to="/project-scoring" class="nav-button">Project Scoring</router-link>
      </nav>
  
      <main class="content">
        <form class="milestone-form" @submit.prevent="handleSubmit">
          <div class="form-group">
            <label for="milestone-name">Milestone Name</label>
            <input id="milestone-name" type="text" placeholder="Type a new milestone to create or select existing milestone to edit or delete" required />
          </div>
  
          <div class="form-group">
            <label for="milestone-description">Milestone Description (Max 50 char)</label>
            <textarea id="milestone-description" placeholder="List the tasks which will form part of this milestone" required></textarea>
          </div>
  
          <div class="form-group">
            <label for="start-date">Milestone Start Date</label>
            <input id="start-date" type="date" required />
          </div>
  
          <div class="form-group">
            <label for="submission-deadline">Submission Deadline</label>
            <input id="submission-deadline" type="date" required />
          </div>
  
          <div class="form-group">
            <label for="max-marks">Max Marks</label>
            <input id="max-marks" type="number" required />
          </div>
  
          <div class="form-actions">
            <button type="submit" class="submit-btn">Submit</button>
            <button type="button" class="delete-btn" @click="confirmDelete">Delete</button>
            <button type="button" class="cancel-btn">Cancel</button>
          </div>
        </form>
      </main>
    </div>
  </template>
  
  <script>
  export default {
    name: 'DefineMilestones',
    methods: {
      confirmDelete() {
        if (confirm('Are you sure you want to delete this milestone?')) {
          // Handle delete action
        }
      },
      handleSubmit() {
        // Handle form submission here
      }
    }
  }
  </script>
  
  <style scoped>
  /* Style remains the same as before */
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
  
  .content {
    padding: 20px;
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
  </style>
  