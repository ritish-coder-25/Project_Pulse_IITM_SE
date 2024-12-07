<script setup>
import {
  BListGroup,
  BListGroupItem,
  BLink,
  BCard,
  BCardBody,
  BCardTitle,
  BCardText,
  BButton,
} from 'bootstrap-vue-next'
</script>

<template>
  <div class="milestone-info">
    <h2>DEADLINES:</h2>
    <div class="deadline-holder">
      <BCard
        v-for="milestone in milestones"
        :key="milestone.id"
        class="mb-4"
        border-variant="primary"
        bg-variant="light"
        :class="{
          'border-success border-box-sh rounded':
            milestone.compStatus === MileStoneStatusEnums.notSubmitted,
          'border-danger':
            milestone.compStatus === MileStoneStatusEnums.deadlineCrossed,
          // 'border-info':
          //   milestone.compStatus === MileStoneStatusEnums.notSubmitted,
        }"
      >
        <BCardBody>
          <BCardTitle tag="h5" class="text-success">{{
            milestone.name
          }}</BCardTitle>
          <BCardText class="text-muted">{{ milestone.description }}</BCardText>

          <ul class="list-unstyled mt-3 mb-4">
            <li>
              <strong>From:</strong> {{ formatDate(milestone.startDate) }}
            </li>
            <li><strong>To:</strong> {{ formatDate(milestone.endDate) }}</li>
            <li>
              <strong>Duration:</strong>
              <span class="badge bg-info text-dark">
                {{ calculateDuration(milestone.startDate, milestone.endDate) }}
                days
              </span>
            </li>
            <li>
              <strong>Max Marks:</strong>
              <span class="badge bg-warning text-dark">{{
                milestone.maxMarks
              }}</span>
            </li>
          </ul>
        </BCardBody>
      </BCard>
    </div>
    <h2>Project Statement:</h2>
    <p class="project-title">Tracking Student Progress in Software Projects</p>
    <p class="project-description">
      In course projects such as the ones you have already done in Application
      Development I and II, it can be challenging for instructors to effectively
      track the progress of student projects, particularly in larger classes
      where multiple teams are working on different tasks...
    </p>
  </div>
</template>

<script>
import { onMounted } from 'vue'
import { MileStoneService } from '../../services/Milestones/milestonesService'
import { MileStoneStatusEnums } from '@/enums'
import { Emitter, Events } from '@/Events'

export default {
  name: 'MilestoneInfo',
  data() {
    return {
      milestones: [],
    }
  },
  methods: {
    async fetchMilestones() {
      // Fetch milestones from API
      // this.milestones = await fetchMilestones();
      const conveMilestones = await MileStoneService.getOnlyMilestones()
      //console.log('converted return milestones', conveMilestones)
      this.milestones = conveMilestones
    },
    formatDate(date) {
      return new Date(date).toLocaleDateString(undefined, {
        year: 'numeric',
        month: 'short',
        day: 'numeric',
      })
    },
    calculateDuration(start, end) {
      const diffTime = Math.abs(new Date(end) - new Date(start))
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24))
      return diffDays
    },
  },
  async mounted() {
    await this.fetchMilestones()
  },
}
</script>

<style scoped>
.milestone-info {
  font-family: 'Arial', sans-serif;
  color: #333;
  background-color: #f9f9fb;
  border: 1px solid #e0e0e0;
  border-radius: 8px;
  padding: 24px;
  margin: 0 auto;
  box-shadow: 0px 4px 12px rgba(0, 0, 0, 0.05);
}

h5 {
  font-size: 20px;
  font-weight: 600;
  color: #2c3e50;
  border-bottom: 2px solid #e0e0e0;
  padding-bottom: 8px;
  margin-top: 24px;
  margin-bottom: 16px;
}

.list-group {
  list-style-type: none;
  padding-left: 0;
  margin-bottom: 24px;
}

.list-group .list-group-item {
  font-size: 16px;
  line-height: 1.8;
  color: #34495e;
  padding: 8px 0;
  border-left: 4px solid #3498db;
  padding-left: 12px;
  margin-bottom: 8px;
  background-color: #eef7fd;
  border-radius: 4px;
}

.list-group .list-group-item strong {
  color: #e74c3c;
}

.project-title {
  font-weight: bold;
  font-size: 18px;
  color: #2c3e50;
  margin-top: 20px;
  margin-bottom: 10px;
}

.project-description {
  font-size: 16px;
  line-height: 1.6;
  color: #555;
  background-color: #fafafa;
  padding: 16px;
  border-left: 4px solid #3498db;
  border-radius: 4px;
  box-shadow: inset 0px 1px 2px rgba(0, 0, 0, 0.05);
}

.deadline-holder {
  display: flex;
  gap: 10px;
  flex-wrap: wrap;
}

.border-box-sh {
  box-shadow:  0px 0px 8px 1px black !important;
}

.milestone-info {
  background-color: #f8f9fa;
}

.text-primary {
  border-left: 5px solid #0d6efd;
  padding-left: 10px;
}

.text-success {
  color: #198754 !important;
}

.text-muted {
  color: #6c757d !important;
}

.badge-info {
  background-color: #0d6efd;
  color: #fff;
}

.badge-warning {
  background-color: #ffc107;
  color: #212529;
}

.shadow-sm {
  box-shadow: 0 0.125rem 0.25rem rgba(0, 0, 0, 0.075) !important;
}

@media (max-width: 768px) {
  .mb-4,
  .mb-5 {
    margin-bottom: 1rem !important;
  }
}
</style>
