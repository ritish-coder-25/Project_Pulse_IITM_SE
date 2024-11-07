<script setup>
import { computed } from 'vue'

import SDashboardComponent from './SDashboardComponent.vue'
import IDashboardComponent from './IDashboardComponent.vue'
import { useAuthStore } from '@/stores/authstore'
import { UserRoleEnums } from '@/enums'

const authStore = useAuthStore()

const currentDashboard = computed(() => {
  return authStore.userRole === UserRoleEnums.student
    ? SDashboardComponent
    : IDashboardComponent
})
</script>

<template>
  <div class="container pt-5 custom-dashboard-tabs">
    <component :is="currentDashboard" />
  </div>
</template>


<style>
.custom-dashboard-tabs .custom-tabs .tab-title {
  display: flex;
  align-items: center;
  white-space: nowrap;
}

.custom-dashboard-tabs .custom-tabs .nav.nav-tabs {
  display: flex;
  justify-content: center;
  gap: 1rem;
}

.custom-dashboard-tabs .custom-tabs .nav-link {
  padding: 0.75rem 1.25rem;
  width: auto;
}

.custom-dashboard-tabs .custom-tabs .dashboard-container {
  padding: 1.5rem;
  background-color: #f8f9fa;
  min-height: 100vh;
}

.custom-dashboard-tabs .custom-tabs {
  background-color: white;
  border-radius: 8px;
  box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
  padding: 1rem 1rem 0 1rem;
}
.custom-dashboard-tabs .custom-tabs .nav-pills {
  border-bottom: 1px solid #dee2e6;
  padding-bottom: 0.5rem;
  gap: 0.5rem;
}

.custom-dashboard-tabs .custom-tabs .nav-link {
  color: #6c757d;
  border-radius: 6px;
  padding: 0.75rem 1.25rem;
  transition: all 0.2s ease-in-out;
}

.custom-dashboard-tabs .custom-tabs .nav-link.active {
  background-color: #0d6efd !important;
  color: white;
  box-shadow: 0 2px 4px rgba(13, 110, 253, 0.2);
}

.custom-dashboard-tabs .custom-tabs .nav-link:hover:not(.active) {
  background-color: #e9ecef !important;
  color: #495057 !important;
}

.custom-dashboard-tabs .custom-tabs .tab-title {
  display: flex;
  align-items: center;
  gap: 0.5rem;
}

.custom-dashboard-tabs .custom-tabs .tab-title > svg.tab-icon {
    height: 1.25rem;
}

.custom-dashboard-tabs .custom-tabs .tab-content-wrapper {
  padding: 1.5rem;
  background-color: white;
  border-radius: 0 0 8px 8px;
}

.custom-dashboard-tabs .custom-tabs .tab-content {
  margin-top: 1rem;
}
</style>
