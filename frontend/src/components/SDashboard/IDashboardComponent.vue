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
import Teams from '../Teams.vue'
import TeamDetails from '../TeamDetails.vue'
import Project_Definition from '../Project_Definition.vue'
import Milestone_Definition from '../Milestone_Definition.vue'
import { useTabRouting } from '@/composables/useTabRouting'
import { RoutesEnums } from '@/enums'

const TabNames = {
  Home: RoutesEnums.dashboard.instructor.home.name,
  MileStoneScoring: RoutesEnums.dashboard.instructor.milestones.name,
  Teams: RoutesEnums.dashboard.instructor.teams.name,
  TeamsDetails: RoutesEnums.dashboard.instructor.teamDetails.name,
  Project_Definition: RoutesEnums.dashboard.instructor.projectDefinition.name,
  Milestone_Definition: RoutesEnums.dashboard.instructor.milestoneDefinition.name,
  Project_Scoring: RoutesEnums.dashboard.instructor.projectScoring.name,
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
      <BTab>
        <template #title>
          <div class="tab-title">
            <UserGroupIcon class="tab-icon me-2" />
            <span>Teams</span>
          </div>
        </template>
        <div class="tab-content-wrapper">
          <Teams />
        </div>
      </BTab>
      <BTab>
        <template #title>
          <div class="tab-title">
            <Milestone class="tab-icon me-2" />
            <span>Define Project</span>
          </div>
        </template>
        <div class="tab-content-wrapper">
          <Project_Definition />
        </div>
      </BTab>
      <BTab>
        <template #title>
          <div class="tab-title">
            <Milestone class="tab-icon me-2" />
            <span>Define Milestone</span>
          </div>
        </template>
        <div class="tab-content-wrapper">
          <Milestone_Definition />
        </div>
      </BTab>
      <!-- <BTab>
        <template #title>
          <div class="tab-title">
            <Milestone class="tab-icon me-2" />
            <span>Project Scoring</span>
          </div>
        </template>
        <div class="tab-content-wrapper">
          <Project_Scoring />
        </div>
      </BTab> -->
    </BTabs>
  </div>
</template>
