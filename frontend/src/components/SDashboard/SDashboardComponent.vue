<script setup>
import { BTabs, BTab } from 'bootstrap-vue-next'
import {
  HomeIcon,
  UserGroupIcon,
  ClipboardDocumentListIcon,
} from '@heroicons/vue/24/outline'
import DefineTeamComponent from '../DefineTeam/DefineTeamComponent.vue'
import MilestoneScoring from '../MilestoneScoring.vue'
</script>

<template>
  <div class="dashboard-container p-4">
    <BTabs class="custom-tabs" nav-class="border-0 mb-3" card>
      <BTab>
        <template #title>
          <div class="tab-title">
            <HomeIcon class="tab-icon me-2" />
            <span>Home</span>
          </div>
        </template>
        <div class="tab-content-wrapper">
          <h1>Student Home</h1>
        </div>
      </BTab>
      <BTab title="Dashboard" active>
        <h1>Student's Dashboard</h1>
      </BTab>
      <BTab title="Define Team" active>
        <h1>DefineTeam</h1>
        <DefineTeamComponent />
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
    </BTabs>
  </div>
</template>
