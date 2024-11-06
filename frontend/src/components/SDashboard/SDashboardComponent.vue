<script setup>
import { BTabs, BTab } from 'bootstrap-vue-next'
import DefineTeamComponent from '../DefineTeam/DefineTeamComponent.vue'
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
    </BTabs>
  </div>
</template>
