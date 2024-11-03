<script setup>
import InputComponent from './InputComponent.vue'
import WelcomeItem from './WelcomeItem.vue'
import DocumentationIcon from './icons/IconDocumentation.vue'
import { LocalStorageEnums } from '../enums'
</script>

<template>
  <div class="container">
    <div class="row mt-5">
      <div class="mx-auto col-4 border p-3 shadow-sm p-3 mb-5 bg-body rounded">
        <form @submit.prevent="handleSubmit">
          <InputComponent
            name="username"
            label="Username:"
            v-model="formData.username"
          ></InputComponent>
          <InputComponent
            name="password"
            label="Password:"
            type="password"
            v-model="formData.password"
          ></InputComponent>
          <button type="submit" class="btn btn-primary">Submit</button>
          <div class="mt-2 text-danger">
            {{ formData.errorCode }}
            {{ formData.errorMessage }}
          </div>
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import InputComponent from './InputComponent.vue'
import { mainAxios } from '../helpers/ApiHelpers'
import { HttpStatusCode } from 'axios'
import { RoutesEnums } from '../enums'
import router from '../router'
import { useAuthStore } from '../stores/authstore'

export default {
  components: { InputComponent },
  data() {
    return {
      formData: {
        username: '',
        password: '',
        errorCode: '',
        errorMessage: ''
      }
    }
  },
  methods: {
    async handleSubmit() {
      const authStore = useAuthStore();
      // handle form submission here
      //this.$emit('submit', this.formData)
      //console.log("form data',",this.formData, this.formData.username,this.formData.password)
      this.formData.errorCode = ''
      this.formData.errorMessage = ''
      try {
        const tokens = await mainAxios.post(
          '/login',
          JSON.stringify({
            username: this.formData.username,
            password: this.formData.password
          })
        )
        console.debug('tokens.', tokens)
        let data = {}
        if (tokens.data) {
          data = JSON.parse(tokens.data)
        }
        if (tokens.status === HttpStatusCode.Ok) {
          console.debug("data",data);
          localStorage.setItem(LocalStorageEnums.accessToken, data.tokens.access_token)
          localStorage.setItem(LocalStorageEnums.refreshToken, data.tokens.refresh_token)
          localStorage.setItem(LocalStorageEnums.user, JSON.stringify(data.user))
          authStore.updateAccessRefreshUser(data.tokens.access_token,data.tokens.refresh_token,data.user)
          router.push(RoutesEnums.start)
          //this.router.push(RoutesEnums.start)
        } else {
          //let data = JSON.parse(tokens.data)
          if (data.error_message) {
            this.formData.errorCode = data['error_code']
            this.formData.errorMessage = data['error_message']
          } else {
            //let innerMessage = JSON.parse(data.message)
            if (data.message.password) {
              //this.formData.errorCode = innerMessage['error_code']
              this.formData.errorMessage = data.message['password']
            } else {
              //this.formData.errorCode = innerMessage['error_code']
              this.formData.errorMessage = data.message['username']
            }
          }
        }
      } catch (err) {
        console.debug('ax', err)
      }

      //this.resetForm()
    },
    resetForm() {
      // reset form data here
      this.formData.username = ''
      this.formData.password = ''
    }
  }
}
</script>
