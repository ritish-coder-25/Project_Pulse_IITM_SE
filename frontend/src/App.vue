<script setup>
import { RouterLink, RouterView } from 'vue-router'

</script>

<template>
  <header class="p-3 bg-dark text-white">
    <div class="container">
      <div
        class="d-flex flex-wrap align-items-center justify-content-center justify-content-lg-start"
      >
        <a
          href="/"
          class="d-flex align-items-center mb-2 mb-lg-0 text-white text-decoration-none"
        >
          <img
            src="@/assets/icon.png"
            alt="Project Pulse Icon"
            width="100"
            height="100"
            class="me-2"
          />
          <svg
            class="bi me-2"
            width="40"
            height="32"
            role="img"
            aria-label="Bootstrap"
          >
            <use xlink:href="#bootstrap"></use>
          </svg>
        </a>

        <ul
          class="nav col-12 col-lg-auto me-lg-auto mb-2 justify-content-center mb-md-0"
        >
          <li>
            <RouterLink class="nav-link px-2 text-white" to="/"
              >Home</RouterLink
            >
          </li>
          <li>
            <RouterLink class="nav-link px-2 text-white" to="/dashboard"
              >Student Dashboard</RouterLink
            >
          </li>
          <li>
            <RouterLink
              class="nav-link px-2 text-white"
              to="/dashboard/instructor"
              >Instructor Dashboard</RouterLink
            >
          </li>
          <!-- <li><a href="#" class="nav-link px-2 text-white">FAQs</a></li>
          <li><a href="#" class="nav-link px-2 text-white">About</a></li> -->
        </ul>

        <!-- <form
          @submit.prevent="handleSubmit"
          class="d-flex col-12 col-lg-auto mb-3 mb-lg-0 me-lg-3"
        >
          <input
            name="search"
            class="form-control me-2"
            type="search"
            placeholder="Search"
            aria-label="Search"
            v-model="formData.search"
          />
          <button class="btn btn-outline-success" type="submit">Search</button>
        </form> -->

        <div class="text-end">
          <RouterLink
            v-if="!isLoggedIn"
            class="btn btn-outline-light me-2"
            to="/login"
            >Login</RouterLink
          >
          <RouterLink
            v-if="!isLoggedIn"
            class="btn btn-outline-light me-2"
            to="/signup"
            >Signup</RouterLink
          >
          <button
            v-if="isLoggedIn"
            type="button"
            class="btn btn-outline-light me-2"
            @click="signout"
          >
            Signout
          </button>
          <!-- <button type="button" class="btn btn-outline-light me-2">Login</button> -->
          <!-- <button type="button" class="btn btn-warning">Sign-up</button> -->
        </div>
      </div>
    </div>
  </header>
  <body class="container-fluid">
    <div class="container mt-3">
    <!-- Warning for inactive approval status -->
    <div v-if="isApproved" class="alert alert-warning" role="alert">
      Your account is currently inactive.Kindly wait for approval from an Admin or TA. For assistance, contact support at <a href="mailto:support@projectpulse.com" class="alert-link">support@projectpulse.com</a>.
    </div>
    </div>
    <RouterView />
  </body>
</template>

<script>
import { mainAxios } from './helpers/ApiHelpers'
import { HttpStatusCode } from 'axios'
import { LocalStorageEnums, RoutesEnums } from './enums'
import router from './router'
import { validateField, validate } from './helpers'
import { useAuthStore } from './stores/authstore'

export default {
  data() {
    return {}
  },
  computed: {
    isLoggedIn() {
      const authStore = useAuthStore()
      console.log("AuthStore",authStore)
      return !!authStore.accessToken
    },
    isApproved() {
      const authStore = useAuthStore()
      const user = authStore.user || {} // Get user from store
      console.log("User --->",user)
      return user.approval_status === 'Inactive'
    },
  },
  watch: {},
  methods: {
    signout() {
      //const authStore = useAuthStore();
      localStorage.removeItem(LocalStorageEnums.accessToken)
      localStorage.removeItem(LocalStorageEnums.refreshToken)
      localStorage.removeItem(LocalStorageEnums.user)
      //authStore.updateAccessRefreshUser(data.tokens.access_token,data.tokens.refresh_token,data.user)
      router.push(RoutesEnums.home)
    },
  },
}
</script>

<!-- <script setup>
import { RouterLink, RouterView } from 'vue-router'
import HelloWorld from './components/HelloWorld.vue'
</script>

<template>
  <header>
    <img
      alt="Vue logo"
      class="logo"
      src="@/assets/logo.svg"
      width="125"
      height="125"
    />

    <div class="wrapper">
      <HelloWorld msg="You did it!" />

      <nav>
        <RouterLink to="/">Home</RouterLink>
        <RouterLink to="/about">About</RouterLink>
      </nav>
    </div>
  </header>

  <RouterView />
</template>

<style scoped>
header {
  line-height: 1.5;
  max-height: 100vh;
}

.logo {
  display: block;
  margin: 0 auto 2rem;
}

nav {
  width: 100%;
  font-size: 12px;
  text-align: center;
  margin-top: 2rem;
}

nav a.router-link-exact-active {
  color: var(--color-text);
}

nav a.router-link-exact-active:hover {
  background-color: transparent;
}

nav a {
  display: inline-block;
  padding: 0 1rem;
  border-left: 1px solid var(--color-border);
}

nav a:first-of-type {
  border: 0;
}

@media (min-width: 1024px) {
  header {
    display: flex;
    place-items: center;
    padding-right: calc(var(--section-gap) / 2);
  }

  .logo {
    margin: 0 2rem 0 0;
  }

  header .wrapper {
    display: flex;
    place-items: flex-start;
    flex-wrap: wrap;
  }

  nav {
    text-align: left;
    margin-left: -1rem;
    font-size: 1rem;

    padding: 1rem 0;
    margin-top: 1rem;
  }
}
</style> -->
