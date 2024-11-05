import { createRouter, createWebHistory } from 'vue-router'
import HomeView from '../views/HomeView.vue'
import { ProtectedRoutesEnums, RoutesEnums } from '../enums/RoutesEnums'
import { LocalStorageEnums } from '@/enums'
import { isJwtTokenExpired } from '@/helpers/TokenHelpers'
import MilestoneScoring from '@/components/MilestoneScoring.vue'
import TAHomepage from '@/components/TAHomepage.vue'

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
      path: '/scoring',
      name: 'MilestoneScoring',
      component: MilestoneScoring
    },
    {
      path: '/tahome',
      name: 'TAHomepage',
      component: TAHomepage
    }
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
