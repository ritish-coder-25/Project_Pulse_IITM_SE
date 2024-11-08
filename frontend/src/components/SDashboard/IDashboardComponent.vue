<script setup>
import { BTabs, BTab } from 'bootstrap-vue-next'
import {
  HomeIcon,
  UserGroupIcon,
  ClipboardDocumentListIcon,
} from '@heroicons/vue/24/outline'
import DefineTeamComponent from '../DefineTeam/DefineTeamComponent.vue'
import MilestoneScoring from '../MilestoneScoring.vue'
import TAHomepage from '../TAHomepage.vue'
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
          <TAHomepage />
        </div>
      </BTab>
      <BTab>
        <template #title>
          <div class="tab-title">
            <UserGroupIcon class="tab-icon me-2" />
            <span>MileStone Scoring</span>
          </div>
        </template>
        <div class="tab-content-wrapper">
          <MilestoneScoring />
        </div>
      </BTab>
    </BTabs>
  </div>
</template>