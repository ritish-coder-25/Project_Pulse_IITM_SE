import { ref, computed } from 'vue'
import { defineStore } from 'pinia'
import { LocalStorageEnums } from '../enums'
import { UserRoleEnums } from '@/enums/UserRoleEnums'

export const useAuthStore = defineStore('authStore', () => {
  const accessToken = ref(localStorage.getItem(LocalStorageEnums.accessToken))
  const refreshToken = ref(localStorage.getItem(LocalStorageEnums.refreshToken))
  const user = ref(
    localStorage.getItem(LocalStorageEnums.user)
      ? JSON.parse(localStorage.getItem(LocalStorageEnums.user))
      : {
          id: null,
          username: null,
          email: null,
          role: UserRoleEnums.student,
        },
  )
  const userRole = computed(() => user.value?.role)
  function updateAccessToken(newAccessToken) {
    accessToken.value = newAccessToken
  }

  function updateRefreshtoken(newRefreshToken) {
    refreshToken.value = newRefreshToken
  }

  function updateuser(newUser) {
    user.value = newUser
  }

  function updateAccessRefresh(newAccessToken, newRefreshToken) {
    accessToken.value = newAccessToken
    refreshToken.value = newRefreshToken
  }
  function updateAccessRefreshUser(newAccessToken, newRefreshToken, newUser) {
    accessToken.value = newAccessToken
    refreshToken.value = newRefreshToken
    user.value = newUser
  }

  return {
    accessToken,
    refreshToken,
    user,
    userRole,
    updateAccessRefresh,
    updateAccessRefreshUser,
    updateuser,
    updateAccessToken,
    updateRefreshtoken,
  }
})
