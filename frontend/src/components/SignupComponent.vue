<script setup>
import InputComponent from './InputComponent.vue'
import router from '../router'
</script>

<template>
  <div class="container">
    <div class="row mt-5">
      <div class="mx-auto col-6 p-4 shadow-sm rounded bg-light form-container">
        <!-- Header Section with Logo and Welcome Message -->
        <div class="header-section">
          <div class="app-logo">App Logo</div>
          <div class="welcome-text">Welcome user! You are not signed in.</div>
        </div>

        <!-- Signup Form -->
        <form @submit.prevent="handleSubmit">
          <label class="form-label">Username</label>
          <input type="text" class="form-control mb-3" v-model="formData.username" />
          
          <label class="form-label">Password</label>
          <input type="password" class="form-control mb-3" v-model="formData.password" />

          <label class="form-label">Reenter Password</label>
          <input type="password" class="form-control mb-3" v-model="formData.reenterPassword" />

          <label class="form-label">Student Email ID</label>
          <input type="email" class="form-control mb-3" v-model="formData.email" />

          <div class="row">
            <div class="col">
              <label class="form-label">GitHub Username</label>
              <input type="text" class="form-control mb-3" v-model="formData.githubUsername" placeholder="(System validates from GitHub)" />
            </div>
            <div class="col">
              <label class="form-label">Discord Username</label>
              <input type="text" class="form-control mb-3" v-model="formData.discordUsername" />
            </div>
          </div>

          <!-- Submit Button -->
          <button type="submit" class="submit-button">Submit</button>
        </form>

        <!-- Link to Login Page -->
        <div class="text-center mt-3">
          <a @click.prevent="redirectToLogin" href="#" class="back-link">Back to Login Page</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>

export default {
  data() {
    return {
      formData: {
        username: '',
        password: '',
        reenterPassword: '',
        email: '',
        githubUsername: '',
        discordUsername: ''
      }
    }
  },
  methods: {
    async handleSubmit() {
      if (this.formData.password !== this.formData.reenterPassword) {
        alert('Passwords do not match');
        return;
      }
      alert('Registration successful!');
      router.push('/login');
    },
    redirectToLogin() {
      router.push('/login');
    }
  }
}
</script>

<style scoped>
.container {
  font-family: Arial, sans-serif;
}

.form-container {
  max-width: 600px;
  padding: 20px;
  border: 1px solid #ccc;
  background-color: #f9f9f9;
}

.header-section {
  display: flex;
  justify-content: space-between;
  align-items: center;
  background-color: #7f7f7f;
  padding: 15px;
  border-radius: 5px 5px 0 0;
  color: white;
}

.app-logo {
  font-weight: bold;
}

.welcome-text {
  font-size: 0.9em;
}

.register-title {
  background-color: #7f7f7f;
  color: white;
  font-size: 1.2em;
  padding: 8px 30px;
  border-radius: 5px;
  border: none;
}

.form-label {
  font-weight: bold;
}

.form-control {
  border: 1px solid #ccc;
  border-radius: 4px;
  padding: 8px;
  font-size: 1em;
}

.submit-button {
  width: 100%;
  padding: 10px;
  font-size: 1em;
  background-color: #7f7f7f;
  color: white;
  border: none;
  border-radius: 5px;
  margin-top: 15px;
}

.back-link {
  color: #007bff;
  font-size: 0.9em;
  text-decoration: underline;
  cursor: pointer;
}
</style>
