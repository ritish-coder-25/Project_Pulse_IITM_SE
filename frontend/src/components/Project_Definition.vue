<template>
    <div class="container">
      <!-- Header with App Logo and User Info -->
      <div class="header">
        <div class="app-logo">App Logo</div>
        <div class="user-info">
          <span>Welcome XXX! You are signed in as TA/Instructor.</span>
          <a href="#" class="logout">Logout</a>
        </div>
      </div>
  
      <!-- Navigation Bar -->
      <div class="navbar">
        <router-link to="/home" class="nav-button">Home</router-link>
        <router-link to="/dashboard" class="nav-button">Dashboard</router-link>
        <router-link to="/define-project" class="nav-button active">Define Project</router-link>
        <router-link to="/project-scoring" class="nav-button">Project Scoring</router-link>
      </div>
  
      <!-- Project Definition Form -->
      <div class="form-container">
        <form @submit.prevent="handleSubmit">
          <!-- Project Name -->
          <label for="project-name">Project Name</label>
          <input id="project-name" type="text" v-model="projectName" required />
  
          <!-- Project Statement -->
          <label for="project-statement">Project Statement</label>
          <textarea id="project-statement" v-model="projectStatement" placeholder="(List the tasks which will form part of this milestone)" required></textarea>
  
          <!-- Project Document URL -->
          <label for="project-url">Project Document URL</label>
          <input id="project-url" type="text" v-model="projectUrl" required />
  
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
  export default {
    data() {
      return {
        projectName: '',
        projectStatement: '',
        projectUrl: '',
      };
    },
    methods: {
      handleSubmit() {
        // Submit form logic here
        console.log('Form Submitted', this.projectName, this.projectStatement, this.projectUrl);
      },
      handleCancel() {
        // Cancel form logic here, reset form or navigate away
        this.projectName = '';
        this.projectStatement = '';
        this.projectUrl = '';
      },
    },
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
  
  /* Navigation Bar */
  .navbar {
    display: flex;
    background-color: #ddd;
    padding: 10px 0;
    justify-content: space-around;
  }
  
  .nav-button {
    padding: 10px 20px;
    border: none;
    background-color: #666;
    color: #fff;
    cursor: pointer;
    font-size: 1em;
  }
  
  .nav-button.active {
    background-color: #b8b28b;
  }
  
  .nav-button:hover {
    background-color: #888;
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
  