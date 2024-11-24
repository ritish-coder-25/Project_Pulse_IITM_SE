import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import { ProtectedRoutesEnums, RoutesEnums } from '../enums/RoutesEnums'
import { LocalStorageEnums, UserRoleEnums } from '@/enums'
import { isJwtTokenExpired } from '@/helpers/TokenHelpers'
import MilestoneScoring from '@/components/MilestoneScoring.vue'
import ProjectDefinition from '@/components/Project_Definition.vue'
import MilestoneDefinition from '@/components/Milestone_Definition.vue'
import StudentTeamsDashboard from '@/components/StudentTeamsDashboard.vue'
import DefineTeamComponent from '@/components/DefineTeam/DefineTeamComponent.vue'
import { useAuthStore } from '@/stores/authstore' // Add this import
import ManageMilestone from '@/components/ManageMilestone.vue'
import MilestoneInfo from '@/components/MilestoneInfo.vue'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: RoutesEnums.home,
      name: 'home',
      component: HomeView,
    },
    {
      path: RoutesEnums.about,
      name: 'about',
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: RoutesEnums.login,
      name: 'login',
      component: () => import('../views/AuthViews/LoginView.vue'),
    },
    {
      path: RoutesEnums.signup,
      name: 'signup',
      component: () => import('../views/AuthViews/SignupView.vue'),
    },
    {
      path: RoutesEnums.dashboard.root.url,  // This is '/dashboard'
      name: RoutesEnums.dashboard.root.name,
      component: () => import('../views/Dashboards/DashboardView.vue'),
      children: [
        {
          path: 'student',  // This is '/dashboard/student'
          redirect: () => {
            const authStore = useAuthStore()
            const u_id = authStore.user.id
            return `/dashboard/student/home/${u_id}`  // Redirect to the home path with user ID
          },
        },
        {
          path: 'student/home/:u_id',  // This is '/dashboard/student/home/:u_id'
          name: RoutesEnums.dashboard.student.home.name,
          component: StudentTeamsDashboard,
          props: true,
        },
        {
          path: 'student/team',
          name: RoutesEnums.dashboard.student.team.name,
          //component: DefineTeamComponent,
        },
        {
          path: 'student/milestones',
          name: RoutesEnums.dashboard.student.milestones.name,
          //component: MilestoneScoring,
        },
        {
          path: 'student/milestoneinfo',
          name: RoutesEnums.dashboard.student.milestoneinfo.name,
          component: MilestoneInfo,
        },
        {
          path: 'student/managemilestone',
          name: RoutesEnums.dashboard.student.managemilestone.name,
          component: ManageMilestone,
        },
        {
          path: 'instructor',  // This is '/dashboard/instructor'
          children: [
            {
              path: '',
              redirect: '/dashboard/instructor/home',  // Redirect to home path of instructor
            },
            {
              path: 'home',
              name: RoutesEnums.dashboard.instructor.home.name,
              //component: TAHomepage,
            },
            {
              path: 'milestones',
              name: RoutesEnums.dashboard.instructor.milestones.name,
              //component: MilestoneScoring,
            },
            {
              path: 'teams',
              name: RoutesEnums.dashboard.instructor.teams.name,
              //component: Teams,
            },
            {
              path: 'team-details',
              name: RoutesEnums.dashboard.instructor.teamDetails.name,
              //component: TeamDetails,
            },
          ],
        },
        {
          path: '',
          redirect() {
            const authStore = useAuthStore()
            return authStore.userRole === UserRoleEnums.student
              ? '/dashboard/student'  // If user is student, go to the student dashboard
              : '/dashboard/instructor'  // Else go to the instructor dashboard
          },
        },
      ],
    },
    {
      path: '/project-definition',
      name: 'ProjectDefinition',
      component: ProjectDefinition,
    },
    {
      path: '/milestone-definition',
      name: 'MilestoneDefinition',
      component: MilestoneDefinition,
    },
    {
      path: '/team/:id',
      name: 'TeamDetails',
      component: () => import('../views/TeamDetailsView.vue'),
    },
    {
      path: '/manage-milestone',
      name: 'ManageMilestone',
      component: ManageMilestone,
    },
    {
      path: '/milestone-info',
      name: 'MilestoneInfo',
      component: MilestoneInfo,
    },
  ],
})

router.beforeEach((to, from, next) => {
  const accessToken = localStorage.getItem(LocalStorageEnums.accessToken)
  const refreshToken = localStorage.getItem(LocalStorageEnums.refreshToken)

  try {
    if (ProtectedRoutesEnums.some((val) => to.fullPath === val)) {
      if (!accessToken || isJwtTokenExpired(refreshToken)) {
        return next(RoutesEnums.login)
      }
    }
    if (to.fullPath === RoutesEnums.login) {
      if (accessToken && !isJwtTokenExpired(refreshToken)) {
        return next(RoutesEnums.start)
      }
    }
  } catch (err) {
    console.debug('router error', err)
  }

  return next()
})

export default router
