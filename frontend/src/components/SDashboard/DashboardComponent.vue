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
  <component :is="currentDashboard" />
</template>
