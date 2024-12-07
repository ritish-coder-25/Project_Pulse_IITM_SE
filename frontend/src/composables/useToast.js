// src/composables/useToast.js
import { useToastController } from 'bootstrap-vue-next'

export function useToast() {
  const { show, remove, toasts } = useToastController()
  const showToast = ({ title, body, variant = 'danger', delay = 3000 }) => {
    console.log('my toast trigger', title, body, variant, delay)
    const showValue = show?.({
      props: {
        title: title,
        body: body,
        value: true,
        variant: variant,
        //pos: 'bottom-center',
      },
    })
    //console.log('found toasts', toasts)
    setTimeout(() => {
      //removeToast(showValue)
      remove?.(showValue)
    }, delay)
  }

  const removeToast = showValue => {
    remove?.(showValue)
  }

  return {
    showToast,
    removeToast,
  }
}
