<script setup>
import { BTabs, BTab } from 'bootstrap-vue-next'
import DefineTeamComponent from '../DefineTeam/DefineTeamComponent.vue'
import MilestoneScoring from '../MilestoneScoring.vue'
import TAHomepage from '../TAHomepage.vue'
</script>

<template>
  <div class="container">
    <BTabs class="mt-5">
      <BTab title="Home" active>
        <h1>Home</h1>
        <TAHomepage />
      </BTab>
      <BTab title="MileStone Scoring" active>
        <h1>MileStone Scoring</h1>
        <MilestoneScoring />
      </BTab>
    </BTabs>
  </div>
</template>
