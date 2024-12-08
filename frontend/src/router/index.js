import { createRouter, createWebHistory, useRoute } from 'vue-router'
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
import { useToast } from '@/composables/useToast'

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: [
    {
      path: RoutesEnums.home,
      name: 'home',
      component: HomeView,
    },
    {
      path: RoutesEnums.homeH,
      name: 'homeH',
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
      path: RoutesEnums.dashboard.root.url, // This is '/dashboard'
      name: RoutesEnums.dashboard.root.name,
      component: () => import('../views/Dashboards/DashboardView.vue'),
      beforeEnter: async (to, from) => {
        // Initialize store outside the navigation guard
        const { showToast } = useToast()
        const authStore = useAuthStore()

        try {
          console.log('Navigation guard triggered:', to.fullPath)

          // Get query parameters
          const query = to.query
          const queryString = Object.keys(query).length
            ? `?${new URLSearchParams(query).toString()}`
            : ''
          console.log(
            'Query string:',
            queryString,
            'authStore:',
            authStore.userRole,
            from.query,
          )

          // Get URL parameters
          const params = to.params
          const urlParams = Object.entries(params)
            .map(([key, value]) => `${value}`)
            .join('')

          console.log('URL params:', urlParams, 'Query params:', queryString)

          // Check user role and redirect
          if (
            to.path.includes('/dashboard') &&
            !to.path.includes('/dashboard/student') &&
            !to.path.includes('/dashboard/instructor')
          ) {
            if (authStore.userRole === UserRoleEnums.student) {
              return `/dashboard/student/home/${urlParams}${queryString}`
            } else if (
              authStore.userRole === UserRoleEnums.instructor ||
              authStore.userRole === UserRoleEnums.ta
            ) {
              return `/dashboard/instructor/home/${urlParams}${queryString}`
            }
            showToast({
              title: 'No role assigned.',
              message: 'Please contact a TA to assign you a role.',
            })
            return `/`
          }
        } catch (error) {
          console.error('Navigation guard error:', error)
          return '/'
        }
      },
      children: [
        {
          path: 'student', // This is '/dashboard/student'
          children: [
            {
              path: '',
              redirect: () => {
                const authStore = useAuthStore()
                const u_id = authStore.user.id
                return `/dashboard/student/home/${u_id ? u_id : ''}` // Redirect to the home path with user ID
              },
            },
            {
              //path: 'home/:u_id?', // This is '/dashboard/student/home/:u_id'
              path: RoutesEnums.dashboard.student.home.url, // This is '/dashboard/student/home/:u_id'
              name: RoutesEnums.dashboard.student.home.name,
              //component: StudentTeamsDashboard,
              props: true,
            },
            {
              //path: 'team/:u_id?',
              path: RoutesEnums.dashboard.student.team.url,
              name: RoutesEnums.dashboard.student.team.name,
              //component: DefineTeamComponent,
            },
            {
              //path: 'milestones/:u_id?',
              path: RoutesEnums.dashboard.student.milestones.url,
              name: RoutesEnums.dashboard.student.milestones.name,
              //component: MilestoneScoring,
            },
            {
              //path: 'milestoneinfo/:u_id?',
              path: RoutesEnums.dashboard.student.milestoneinfo.url,
              name: RoutesEnums.dashboard.student.milestoneinfo.name,
              //component: MilestoneInfo,
            },
            {
              //path: 'managemilestone/:u_id?',
              path: RoutesEnums.dashboard.student.managemilestone.url,
              name: RoutesEnums.dashboard.student.managemilestone.name,
              //component: ManageMilestone,
            },
          ],
        },

        {
          path: 'instructor', // This is '/dashboard/instructor'
          children: [
            {
              path: '',
              redirect: '/dashboard/instructor/home', // Redirect to home path of instructor
            },
            {
              //path: 'home/:u_id?',
              path: RoutesEnums.dashboard.instructor.home.url,
              name: RoutesEnums.dashboard.instructor.home.name,
              //component: TAHomepage,
            },
            {
              //path: 'milestones/:u_id?',
              path: RoutesEnums.dashboard.instructor.milestones.url,
              name: RoutesEnums.dashboard.instructor.milestones.name,
              //component: MilestoneScoring,
            },
            {
              path: RoutesEnums.dashboard.instructor.teams.path,
              name: RoutesEnums.dashboard.instructor.teams.name,
              //component: Teams,
            },
            {
              path: RoutesEnums.dashboard.instructor.projectDefinition.path,
              name: RoutesEnums.dashboard.instructor.projectDefinition.name,
              //component: TeamDetails,
            },
            {
              path: RoutesEnums.dashboard.instructor.milestoneDefinition.path,
              name: RoutesEnums.dashboard.instructor.milestoneDefinition.name,
              //component: TeamDetails,
            },
          ],
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
    if (ProtectedRoutesEnums.some(val => to.fullPath === val)) {
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
