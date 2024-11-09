<script setup>
import { BTabs, BTab } from 'bootstrap-vue-next'
import DefineTeamComponent from '../DefineTeam/DefineTeamComponent.vue'
import ManageMilestone from '../ManageMilestone.vue';
import MilestoneInfo from '../MilestoneInfo.vue';
</script>

<template>
  <div class="container">
    <BTabs class="mt-5">
      <BTab title="Home" active>
        <h1>Home</h1>
      </BTab>
      <BTab title="Define Team" active>
        <h1>DefineTeam</h1>
        <DefineTeamComponent />
      </BTab>
      <BTab title="Manage Milestone" active>
        <h1>Manage Milestone</h1>
        <ManageMilestone/>
      </BTab>
      <BTab title="MilestoneInfo" active>
        <h1>Milestone Info</h1>
        <MilestoneInfo/>
      </BTab>
    </BTabs>
  </div>
</template>
