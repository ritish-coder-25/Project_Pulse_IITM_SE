<script setup>
import InputComponent from './InputComponent.vue'
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
            :errorMessage="errors.username"
          ></InputComponent>
          <InputComponent
            name="email"
            label="Email:"
            type="email"
            v-model="formData.email"
            :errorMessage="errors.email"
          ></InputComponent>
          <InputComponent
            name="first_name"
            label="First name:"
            type="text"
            v-model="formData.first_name"
            :errorMessage="errors.first_name"
          ></InputComponent>
          <InputComponent
            name="last_name"
            label="Last name:"
            type="text"
            v-model="formData.last_name"
            :errorMessage="errors.last_name"
          ></InputComponent>
          <InputComponent
            name="password"
            label="Password:"
            type="password"
            v-model="formData.password"
            :errorMessage="errors.password"
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
import { SignupSchema } from '../YupSchemas'
import { validateField,validate } from '../helpers'

export default {
  components: { InputComponent },
  data() {
    return {
      formData: {
        username: '',
        password: '',
        first_name: '',
        last_name: '',
        email: '',
        errorCode: '',
        errorMessage: ''
      },
      errors: {
        username: '',
        password: '',
        first_name: '',
        last_name: '',
        email: '',
      },
    }
  },
  watch:{
    ["formData.email"]: async function (val,oldVal) {
        //console.debug("oldval",oldVal,"newval",val,this)
        const errors = await validateField(SignupSchema,this.formData,'email',this.errors)
        //console.debug("errors got fro mschema",errors)
        //this.errors.email = errors.message
    },
    ["formData.username"]: async function (val,oldVal) {
        //console.debug("oldval",oldVal,"newval",val,this)
        const errors = await validateField(SignupSchema,this.formData,'username',this.errors)

        //const errors = await validateField(SignupSchema,this.formData,'username',this.errors)
        //console.debug("errors got fro mschema",errors)
        //this.errors.username = errors.message
    },
    ["formData.password"]: async function (val,oldVal) {
        //console.debug("oldval",oldVal,"newval",val,this)
        const errors = await validateField(SignupSchema,this.formData,'password',this.errors)
        //console.debug("errors got fro mschema",errors)
        //this.errors.password = errors.message
    },
    ["formData.first_name"]: async function (val,oldVal) {
        //console.debug("oldval",oldVal,"newval",val,this)
        const errors = await validateField(SignupSchema,this.formData,'first_name',this.errors)
        //console.debug("errors got fro mschema",errors)
        //this.errors["first_name"] = errors.message
    },
    ["formData.last_name"]: async function (val,oldVal) {
        //console.debug("oldval",oldVal,"newval",val,this)
        const errors = await validateField(SignupSchema,this.formData,'last_name',this.errors)
        //console.debug("errors got fro mschema",errors)
        //this.errors["last_name"] = errors.message
    }
  },
  methods: {
    async handleSubmit() {
      const authStore = useAuthStore()
      const isValidData = await validate(SignupSchema,this.formData,this.errors)
      if(!isValidData){
        return
      }
      // handle form submission here
      //this.$emit('submit', this.formData)
      //console.log("form data',",this.formData, this.formData.username,this.formData.password)
      this.formData.errorCode = ''
      this.formData.errorMessage = ''
      try {
        const tokens = await mainAxios.post(
          '/user',
          JSON.stringify({
            username: this.formData.username,
            email: this.formData.email,
            first_name: this.formData.first_name,
            last_name: this.formData.last_name,
            password: this.formData.password
          })
        )
        console.debug('tokens.', tokens)
        let data = {}
        if (tokens.data) {
          data = JSON.parse(tokens.data)
        }
        if (tokens.status === HttpStatusCode.Created) {
          console.debug('data', data)
          localStorage.setItem(LocalStorageEnums.accessToken, data.tokens.access_token)
          localStorage.setItem(LocalStorageEnums.refreshToken, data.tokens.refresh_token)
          localStorage.setItem(LocalStorageEnums.user, JSON.stringify(data.user))
          authStore.updateAccessRefreshUser(
            data.tokens.access_token,
            data.tokens.refresh_token,
            data.user
          )
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
