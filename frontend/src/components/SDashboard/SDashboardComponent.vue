<script setup>
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
import { useTabRouting } from '@/composables/useTabRouting'
import ManageMilestone from '../ManageMilestone.vue'
import MilestoneInfo from '../MilestoneInfo.vue'

const TabNames = {
  Home: RoutesEnums.dashboard.student.home.name,
  DefineTeam: RoutesEnums.dashboard.student.team.name,
  //Milestones: RoutesEnums.dashboard.student.milestones.name,
  MilestoneInfo: RoutesEnums.dashboard.student.milestoneinfo.name,
  ManageMilestone: RoutesEnums.dashboard.student.managemilestone.name,
}

const { activeTab, onTabChange } = useTabRouting(TabNames)
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
      <BTab title="MilestoneInfo">
        <template #title>
          <div class="tab-title">
            <UserGroupIcon class="tab-icon me-2" />
            <span>Milestone Info</span>
          </div>
        </template>
        <div class="tab-content-wrapper">
          <MilestoneInfo />
        </div>
      </BTab>
      <BTab title="Manage Milestone">
        <template #title>
          <div class="tab-title">
            <UserGroupIcon class="tab-icon me-2" />
            <span>Manage Milestone</span>
          </div>
        </template>
        <div class="tab-content-wrapper">
          <ManageMilestone />
        </div>
      </BTab>
    </BTabs>
  </div>
</template>
