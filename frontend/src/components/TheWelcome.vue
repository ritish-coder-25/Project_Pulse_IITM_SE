<script setup>
import { BContainer, BRow, BCol, BCard } from 'bootstrap-vue-next'
import { AcademicCapIcon, UsersIcon, ClipboardIcon, ChartBarIcon } from '@heroicons/vue/24/outline'
</script>

<template>
  <BContainer fluid class="p-0 m-0">
    <!-- Hero Section -->
    <div class="bg-primary text-white py-5">
      <BContainer>
        <BRow class="align-items-center">
          <BCol md="6">
            <h1 class="display-4">Team Project Management</h1>
            <p class="lead">
              Streamline student team assignments, project tracking, and grading for professors
            </p>
          </BCol>
          <BCol md="6">
            <!-- <img src="@/assets/team-collaboration.svg" alt="Collaboration" class="img-fluid" /> -->
          </BCol>
        </BRow>
      </BContainer>
    </div>

    <!-- Features Section -->
    <BContainer class="py-5">
      <h2 class="text-center mb-5">Key Features</h2>
      <BRow>
        <BCol md="3">
          <BCard class="h-100 text-center p-3">
            <UsersIcon class="w-12 h-12 mx-auto mb-3 text-primary" />
            <h4>Team Formation</h4>
            <p>Easily assign students to balanced teams</p>
          </BCard>
        </BCol>
        <BCol md="3">
          <BCard class="h-100 text-center p-3">
            <ClipboardIcon class="w-12 h-12 mx-auto mb-3 text-primary" />
            <h4>Project Details</h4>
            <p>Define projects and milestone requirements</p>
          </BCard>
        </BCol>
        <BCol md="3">
          <BCard class="h-100 text-center p-3">
            <ChartBarIcon class="w-12 h-12 mx-auto mb-3 text-primary" />
            <h4>Progress Tracking</h4>
            <p>Monitor team progress and milestone completion</p>
          </BCard>
        </BCol>
        <BCol md="3">
          <BCard class="h-100 text-center p-3">
            <AcademicCapIcon class="w-12 h-12 mx-auto mb-3 text-primary" />
            <h4>Grading</h4>
            <p>Evaluate and grade milestone submissions</p>
          </BCard>
        </BCol>
      </BRow>
    </BContainer>

    <!-- How It Works -->
    <div class="bg-light py-5">
      <BContainer>
        <h2 class="text-center mb-5">How It Works</h2>
        <BRow class="g-4">
          <BCol md="4">
            <div class="d-flex align-items-center">
              <div class="fs-1 me-3 text-primary">1</div>
              <div>
                <h5>Create Teams</h5>
                <p>Assign students to balanced teams or let them form their own groups</p>
              </div>
            </div>
          </BCol>
          <BCol md="4">
            <div class="d-flex align-items-center">
              <div class="fs-1 me-3 text-primary">2</div>
              <div>
                <h5>Set Milestones</h5>
                <p>Define project requirements and milestone deadlines</p>
              </div>
            </div>
          </BCol>
          <BCol md="4">
            <div class="d-flex align-items-center">
              <div class="fs-1 me-3 text-primary">3</div>
              <div>
                <h5>Track & Grade</h5>
                <p>Monitor progress and evaluate team performance</p>
              </div>
            </div>
          </BCol>
        </BRow>
      </BContainer>
    </div>
  </BContainer>
</template>

<style scoped>
.card {
  transition: transform 0.2s;
}
.card:hover {
  transform: translateY(-5px);
}
</style>
