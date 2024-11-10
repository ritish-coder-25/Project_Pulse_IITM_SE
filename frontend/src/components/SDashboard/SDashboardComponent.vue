<script setup>
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'
import { BTabs, BTab } from 'bootstrap-vue-next'
import {
  HomeIcon,
  UserGroupIcon,
  ClipboardDocumentListIcon,
} from '@heroicons/vue/24/outline'
import DefineTeamComponent from '../DefineTeam/DefineTeamComponent.vue'
import MilestoneScoring from '../MilestoneScoring.vue'
import StudentTeamsDashboard from '../StudentTeamsDashboard.vue'
import { RoutesEnums } from '@/enums'

const router = useRouter()
const route = useRoute()

const TabNames = {
  Home: RoutesEnums.dashboard.student.home.name,
  DefineTeam: RoutesEnums.dashboard.student.team.name,
  //Milestones: RoutesEnums.dashboard.student.milestones.name,
}

const routeToTabIndex = Object.values(TabNames).reduce(
  (acc, tabName, index) => {
    acc[tabName] = index
    return acc
  },
  {},
)
console.log(routeToTabIndex)

const activeTab = ref(routeToTabIndex[route.name] || 0)

// Handle tab changes
const onTabChange = tabIndex => {
  const routes = [...Object.values(TabNames)]
  router.push({ name: routes[tabIndex] })
}

// Keep tabs in sync with route changes
watch(
  () => route.name,
  newRoute => {
    activeTab.value = routeToTabIndex[newRoute] || 0
  },
)
</script>

<template>
  <div class="dashboard-container p-4">
    <BTabs
      class="custom-tabs"
      nav-class="border-0 mb-3"
      card
      v-model="activeTab"
      @update:modelValue="onTabChange"
    >
      <BTab>
        <template #title>
          <div class="tab-title">
            <HomeIcon class="tab-icon me-2" />
            <span>Home</span>
          </div>
        </template>
        <div class="tab-content-wrapper">
          <h1>Student Home</h1>
          <StudentTeamsDashboard />
        </div>
      </BTab>
      <BTab>
        <template #title>
          <div class="tab-title">
            <UserGroupIcon class="tab-icon me-2" />
            <span>Define Team</span>
          </div>
        </template>
        <div class="tab-content-wrapper">
          <DefineTeamComponent />
        </div>
      </BTab>
      <!-- <BTab title="Team's Dashboard" active>
        <h1>Dashboard</h1>
        <StudentTeamsDashboard />
      </BTab> -->
    </BTabs>
  </div>
</template>
