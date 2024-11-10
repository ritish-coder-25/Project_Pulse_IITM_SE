export const RoutesEnums = {
  login: '/login',
  signup: '/signup',
  home: '/',
  about: '/about',
  dashboard: {
    root: { name: 'dashboard', url: '/dashboard' },
    student: {
      root: {
        name: 'student-dashboard-root',
        url: '/dashboard/student',
        relUrl: 'student',
      },
      home: {
        name: 'student-dashboard-home',
        url: '/dashboard/student/home',
        relUrl: 'home',
      },
      team: {
        name: 'student-dashboard-team',
        url: '/dashboard/student/team',
        relUrl: 'team',
      },
      milestones: {
        name: 'student-dashboard-milestones',
        url: '/dashboard/student/milestones',
        relUrl: 'milestones',
      },
    },
    instructor: {
      root: {
        name: 'instructor-dashboard-root',
        url: '/dashboard/instructor',
        relUrl: 'instructor',
      },
      home: {
        name: 'instructor-dashboard-home',
        url: '/dashboard/instructor/home',
        relUrl: 'home',
      },
      milestones: {
        name: 'instructor-dashboard-milestones',
        url: '/dashboard/instructor/milestones',
        relUrl: 'milestones',
      },
      teams: {
        name: 'instructor-dashboard-teams',
        url: '/dashboard/instructor/teams',
        relUrl: 'teams',
      },
      teamDetails: {
        name: 'instructor-dashboard-team-details',
        url: '/dashboard/instructor/team-details',
        relUrl: 'team-details',
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
