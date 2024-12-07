export const RoutesEnums = {
  login: '/login',
  signup: '/signup',
  home: '/',
  homeH: '/home',
  about: '/about',
  dashboard: {
    root: { name: 'dashboard', url: '/dashboard/:id?' },
    student: {
      root: {
        name: 'student-dashboard-root',
        url: `/dashboard/student/home/:u_id?`,
        relUrl: 'student',
      },
      home: {
        name: 'student-dashboard-home',
        url: '/dashboard/student/home/:u_id?',
        relUrl: 'home',
      },
      team: {
        name: 'student-dashboard-team',
        url: '/dashboard/student/team/:u_id?',
        relUrl: 'team',
      },
      milestones: {
        name: 'student-dashboard-milestones',
        url: '/dashboard/student/milestones/:u_id?',
        relUrl: 'milestones',
      },
      milestoneinfo: {
        name: 'student-dashboard-milestoneinfo',
        url: '/dashboard/student/milestoneinfo/:u_id?',
        relUrl: 'milestoneinfo',
      },
      managemilestone: {
        name: 'student-dashboard-managemilestone',
        url: '/dashboard/student/managemilestone/:u_id?',
        relUrl: 'managemilestone',
      },
    },
    instructor: {
      root: {
        name: 'instructor-dashboard-root',
        url: '/dashboard/instructor/:u_id?',
        relUrl: 'instructor',
      },
      home: {
        name: 'instructor-dashboard-home',
        url: '/dashboard/instructor/home/:u_id?',
        relUrl: 'home',
      },
      milestones: {
        name: 'instructor-dashboard-milestones',
        url: '/dashboard/instructor/milestones/:u_id?',
        relUrl: 'milestones',
      },
      teams: {
        name: 'instructor-dashboard-teams',
        url: '/dashboard/instructor/teams/:u_id?',
        path: 'teams/:u_id?',
        relUrl: 'teams',
      },
      teamDetails: {
        name: 'instructor-dashboard-team-details',
        url: '/dashboard/instructor/team-details/:u_id?',
        relUrl: 'team-details',
      },
      projectDefinition: {
        name: 'instructor-project-definition',
        url: '/project-definition/:u_id?',
        path: 'project-definition/:u_id?',
        reUrl: 'project-definition',
      },
      milestoneDefinition: {
        name: 'instructor-milestone-definition',
        url: '/milestone-definition/:u_id?',
        path: 'milestone-definition/:u_id?',
        reUrl: 'milestone-definition'
      },
      projectScoring: {
        name: 'instructor-project-scoring',
        url: '/scoring/:u_id?',
        reUrl: 'project-scoring'
      },
    }
  },
}

export const ProtectedRoutesEnums = []

export const UnProtectedRoutesEnums = [
  RoutesEnums.login,
  RoutesEnums.signup,
  RoutesEnums.home,
  RoutesEnums.about,
]
