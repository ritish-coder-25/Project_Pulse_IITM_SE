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
  },
}

export const ProtectedRoutesEnums = []

export const UnProtectedRoutesEnums = [
  RoutesEnums.login,
  RoutesEnums.signup,
  RoutesEnums.home,
  RoutesEnums.about,
]
