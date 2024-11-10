// src/composables/useTabRouting.js
import { ref, watch } from 'vue'
import { useRoute, useRouter } from 'vue-router'

export function useTabRouting(tabNames) {
  const route = useRoute()
  const router = useRouter()

  const routeToTabIndex = Object.values(tabNames).reduce(
    (acc, tabName, index) => {
      acc[tabName] = index
      return acc
    },
    {},
  )

  const activeTab = ref(routeToTabIndex[route.name] || 0)

  const onTabChange = tabIndex => {
    const routes = [...Object.values(tabNames)]
    router.push({ name: routes[tabIndex] })
  }

  watch(
    () => route.name,
    newRoute => {
      activeTab.value = routeToTabIndex[newRoute] || 0
    },
  )

  return {
    activeTab,
    onTabChange,
  }
}
