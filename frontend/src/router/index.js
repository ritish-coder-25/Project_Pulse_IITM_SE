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
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AboutView.vue'),
    },
    {
      path: RoutesEnums.login,
      name: 'login',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AuthViews/LoginView.vue'),
    },
    {
      path: RoutesEnums.signup,
      name: 'signup',
      // route level code-splitting
      // this generates a separate chunk (About.[hash].js) for this route
      // which is lazy-loaded when the route is visited.
      component: () => import('../views/AuthViews/SignupView.vue'),
    },
    {
      path: RoutesEnums.dashboard.root.url,
      name: RoutesEnums.dashboard.root.name,
      component: () => import('../views/Dashboards/DashboardView.vue'),
      children: [
        {
          path: RoutesEnums.dashboard.student.root.relUrl,
          //component: SDashboardComponent,
          children: [
            {
              path: '',
              name: RoutesEnums.dashboard.student.root.name,
              redirect: '/dashboard/student/home',
            },
            {
              path: RoutesEnums.dashboard.student.home.relUrl,
              name: RoutesEnums.dashboard.student.home.name,
              //component: StudentTeamsDashboard,
            },
            {
              path: RoutesEnums.dashboard.student.team.relUrl,
              name: RoutesEnums.dashboard.student.team.name,
              //component: DefineTeamComponent,
            },
            {
              path: RoutesEnums.dashboard.student.milestones.relUrl,
              name: RoutesEnums.dashboard.student.milestones.name,
              //component: MilestoneScoring,
            },
          ],
        },
        // {
        //   path: 'instructor',
        //   //component: IDashboardComponent,
        //   children: [
        //     {
        //       path: '',
        //       redirect: '/dashboard/instructor/home',
        //     },
        //     {
        //       path: 'home',
        //       name: 'instructor-dashboard-home',
        //       //component: TAHomepage,
        //     },
        //     {
        //       path: 'milestones',
        //       name: 'instructor-dashboard-milestones',
        //       //component: MilestoneScoring,
        //     },
        //     {
        //       path: 'teams',
        //       name: 'instructor-dashboard-teams',
        //       //component: Teams,
        //     },
        //     {
        //       path: 'team-details',
        //       name: 'instructor-dashboard-team-details',
        //       //component: TeamDetails,
        //     },
        //   ],
        // },
        {
          path: '',
          redirect: to => {
            // Get user role from store/localStorage
            const authStore = useAuthStore()
            return authStore.userRole === UserRoleEnums.student
              ? '/dashboard/student'
              : '/dashboard/instructor'
          },
        },
      ],
    },
    {
      path: '/project-definition',
      name: 'ProjectDefinition',
      component: ProjectDefinition, // If eagerly loaded
      // Or use lazy loading with:
      // component: () => import('@/components/Project_Definition.vue')
    },
    {
      path: '/milestone-definition',
      name: 'MilestoneDefinition',
      component: MilestoneDefinition, // Add route for DefineMilestones
    },
    {
      path: '/team/:id',
      name: 'TeamDetails',
      component: () => import('../views/TeamDetailsView.vue'), // Add route for DefineMilestones
    },
  ],
})

router.beforeEach((to, from, next) => {
  const accessToken = localStorage.getItem(LocalStorageEnums.accessToken, null)
  const refreshToken = localStorage.getItem(
    LocalStorageEnums.refreshToken,
    null,
  )
  const accessTokenExpired = isJwtTokenExpired(accessToken)
  const refreshTokenExpired = isJwtTokenExpired(refreshToken)

  try {
    if (
      ProtectedRoutesEnums.findIndex(val => {
        if (to.fullPath === val) {
          return true
        }
      }) != -1
    ) {
      if (!accessToken || refreshTokenExpired) {
        return next(RoutesEnums.login)
      }
    }
    if (to.fullPath === RoutesEnums.login) {
      if (accessToken && !refreshTokenExpired) {
        return next(RoutesEnums.start)
      }
    }
  } catch (err) {
    console.debug('router error', err)
  }

  // next();
  return next()
})

export default router
