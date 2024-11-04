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

        <!-- Login Title -->
        <div class="text-center mb-3">
          <button class="login-title">Login</button>
        </div>

        <!-- Login Form -->
        <form @submit.prevent="handleSubmit">
          <label class="form-label">Username</label>
          <input type="text" class="form-control mb-3" v-model="formData.username" />

          <label class="form-label">Password</label>
          <input type="password" class="form-control mb-3" v-model="formData.password" />

          <div class="d-flex justify-content-around mt-3">
            <button type="submit" class="submit-button">Submit</button>
            <button type="button" @click="resetForm" class="submit-button">Reset</button>
          </div>
        </form>

        <!-- Register Link -->
        <div class="text-center mt-3">
          <a @click.prevent="redirectToRegister" href="#" class="back-link">Register as new user</a>
        </div>
      </div>
    </div>
  </div>
</template>

<script>
import { useAuthStore } from '../stores/authstore'

export default {
  data() {
    return {
      formData: {
        username: '',
        password: ''
      }
    }
  },
  methods: {
    async handleSubmit() {
      alert('Login successful!');
      router.push('/dashboard');
    },
    resetForm() {
      this.formData.username = '';
      this.formData.password = '';
    },
    redirectToRegister() {
      router.push('/register');
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

.login-title {
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
  width: 45%;
  padding: 10px;
  font-size: 1em;
  background-color: #7f7f7f;
  color: white;
  border: none;
  border-radius: 5px;
}

.back-link {
  color: #007bff;
  font-size: 0.9em;
  text-decoration: underline;
  cursor: pointer;
}
</style>
