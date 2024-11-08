import { createRouter, createWebHistory } from 'vue-router';
import HomeView from '../views/HomeView.vue';
import { ProtectedRoutesEnums, RoutesEnums } from '../enums/RoutesEnums';
import { LocalStorageEnums } from '@/enums';
import { isJwtTokenExpired } from '@/helpers/TokenHelpers';
import MilestoneScoring from '@/components/MilestoneScoring.vue';
import ProjectDefinition from '@/components/Project_Definition.vue';
import MilestoneDefinition from '@/components/Milestone_Definition.vue';
import ManageMilestone from '@/components/ManageMilestone.vue';

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
      path: '/dashboard',
      name: 'dashboard',
      component: () => import('../views/Dashboards/DashboardView.vue'),
    },
    {
      path: '/scoring',
      name: 'MilestoneScoring',
      component: MilestoneScoring,
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
      path: '/manage-milestone',
      name: 'ManageMilestone',
      component: ManageMilestone,
    },
  ],
});

router.beforeEach((to, from, next) => {
  const accessToken = localStorage.getItem(LocalStorageEnums.accessToken);
  const refreshToken = localStorage.getItem(LocalStorageEnums.refreshToken);
  const accessTokenExpired = isJwtTokenExpired(accessToken);
  const refreshTokenExpired = isJwtTokenExpired(refreshToken);

  try {
    if (ProtectedRoutesEnums.some(val => to.fullPath === val)) {
      if (!accessToken || refreshTokenExpired) {
        return next(RoutesEnums.login);
      }
    }
    if (to.fullPath === RoutesEnums.login) {
      if (accessToken && !refreshTokenExpired) {
        return next(RoutesEnums.start);
      }
    }
  } catch (err) {
    console.debug('router error', err);
  }

  return next();
});

export default router;
