<script setup>
import { Form, Field, ErrorMessage } from 'vee-validate'
</script>

<template>
  <div>
    <div class="row mt-5">
      <FormConatiner>
        <Form
          :validation-schema="DefineTeamSchema"
          @submit="onSubmit"
          v-slot="{
            values,
            setFieldValue,
            resetForm,
            errors,
            resetField,
            setValues,
          }"
          :validate-on-mount="false"
        >
          <div
            v-if="
              storeFormRefs({
                resetForm,
                setFieldValue,
                resetField,
                setValues,
                values,
              })
            "
          ></div>
          <div class="mb-3">
            <label class="form-label" for="team-input">Team Name</label>
            <Field name="team" v-slot="{ field, meta }">
              <input
                v-bind="field"
                id="team-input"
                class="form-control"
                :readonly="isTeamReadOnly"
                placeholder="Enter team name"
                :class="{
                  'is-invalid': meta.touched && meta.errors.length > 0,
                }"
              />
              <div class="invalid-feedback">
                <ErrorMessage name="team" v-if="meta.touched" />
              </div>
            </Field>
          </div>

          <div class="mb-3">
            <label class="form-label" for="team-input">Github Repo Url</label>
            <Field name="github_repo_url" v-slot="{ field, meta }">
              <input
                v-bind="field"
                id="github-repo-input"
                class="form-control"
                :readonly="isTeamReadOnly"
                placeholder="Enter repo url"
                :class="{
                  'is-invalid': meta.touched && meta.errors.length > 0,
                }"
              />
              <div class="invalid-feedback">
                <ErrorMessage name="github_repo_url" v-if="meta.touched" />
              </div>
            </Field>
          </div>

          <!-- Dynamic Email Dropdowns -->
          <div
            v-for="(field, index) in emailFields"
            :key="field.key"
            class="mb-3"
          >
            <label class="form-label">Email {{ index + 1 }}</label>
            <div class="input-group">
              <Field :name="`emails.${index}`" v-slot="{ field, meta }">
                <div class="position-relative w-100">
                  <div>
                    <div class="d-flex">
                      <input
                        type="text"
                        v-bind="field"
                        class="form-control"
                        :class="{
                          'is-invalid': meta.touched && meta.errors.length > 0,
                        }"
                        @input="
                          e => {
                            debounceSearch(e, index)
                          }
                        "
                        placeholder="Search email..."
                      />
                      <button
                        type="button"
                        class="btn btn-danger ms-2"
                        @click="removeEmail(index, setFieldValue)"
                        v-if="emailFields.length > 1"
                      >
                        <i class="bi bi-trash"></i>
                      </button>
                    </div>
                    <div
                      :class="{
                        'is-invalid': meta.touched && meta.errors.length > 0,
                      }"
                    ></div>
                    <div class="invalid-feedback">
                      {{ errors[`emails[${index}]`] }}
                      <ErrorMessage
                        :name="`emails[${index}]`"
                        v-if="
                          meta.touched && searchResults[index]?.length === 0
                        "
                      />
                    </div>
                  </div>

                  <!-- Results Dropdown -->
                  <div
                    v-if="searchResults[index]?.length"
                    class="position-absolute w-100 bg-white border rounded-bottom shadow-sm"
                    style="z-index: 1000"
                  >
                    <div
                      v-for="result in searchResults[index]"
                      :key="result.email"
                      class="p-2 cursor-pointer hover:bg-gray-100"
                      @click="
                        () => {
                          //field.value = result.email
                          selectEmail(
                            result.email,
                            result.id,
                            index,
                            setFieldValue,
                          )
                        }
                      "
                    >
                      <div class="d-flex flex-column">
                        <span class="fw-bold">{{ result.email }}</span>
                        <small class="text-muted">
                          {{ result.first_name }} {{ result.last_name }}
                        </small>
                      </div>
                    </div>
                  </div>
                </div>
              </Field>
            </div>
          </div>
          <div class="invalid-feedback d-block" v-if="errors?.emails">
            {{ errors?.emails }}
          </div>

          <!-- Buttons Container -->
          <div class="text-end">
            <button
              type="button"
              class="btn btn-primary mb-4 d-block ms-auto"
              @click="addEmail"
            >
              <i class="bi bi-plus-circle"></i>
            </button>

            <button type="submit" class="btn btn-primary d-block ms-auto">
              Submit
            </button>
          </div>
        </Form>
      </FormConatiner>
    </div>
  </div>
</template>

<script>
import { DefineTeamApiHelper } from '@/helpers/ApiHelperFuncs/DefineTeam'
import { useForm, useFieldArray } from 'vee-validate'
import { DefineTeamSchema } from '@/YupSchemas'
import FormConatiner from '../MainComponents/FormConatiner.vue'
import { mainAxios } from '@/helpers'
import { LocalStorageEnums } from '@/enums'
import { DefineTeamService } from '../../../services'

export default {
  name: 'DefineTeamComponent',
  data() {
    return {
      emailOptions: [],
      isTeamReadOnly: false,
      emailFields: [],
      updateEmailField: null,
      searchResults: {},
      searchTimeout: null,
      formData: null,
      push: null,
      remove: null,
      reset: null,
      handleSubmit: null,
      errors: null,
      values: null,
      //setFieldValue: null,
      setValues: null,
      resetFormRef: null,
      setFieldValueRef: null,
      resetFieldRef: null,
      setValuesRef: null,
      currentTeam: null,
      valuesRef: null,
    }
  },
  created() {
    // Initialize form
    const {
      handleSubmit,
      reset,
      setErrors,
      errors,
      values,
      setValues,
      setFieldValue,
      resetField,
    } = useForm({
      validationSchema: DefineTeamSchema,
      initialValues: {
        team: '',
        emails: [''],
        github_repo_url: '',
      },
      validateOnMount: false,
      initialTouched: false,
      initialErrors: {},
    })
    //setValues({team: 'testing', emails: ['hiii']})
    // Initialize field array
    const { fields, push, remove, update } = useFieldArray('emails')
    // Assign to data properties
    this.emailFields = fields
    this.push = push
    this.remove = remove
    this.reset = reset
    this.handleSubmit = handleSubmit
    this.errors = errors
    this.values = values
    this.updateEmailField = update
    //this.setFieldValue = setFieldValue
    this.setValues = setValues
  },
  methods: {
    resetForm() {
      this.reset()
      this.isTeamReadOnly = false
    },
    addEmail() {
      this.push('')
    },
    async removeEmail(index, setFieldValue) {
      console.log("this.currentTeam", this.currentTeam);
      await DefineTeamService.removeEmail({
        index,
        setFieldValue,
        valuesRef: this.valuesRef,
        currentTeam: this.currentTeam,
        emailFields: this.emailFields,
        remove: this.remove,
      })
    },
    async onSubmit(formValues) { 
      if (this.currentTeam) {
        formValues.team_id = this.currentTeam.teamId
        const formResult = await DefineTeamApiHelper.updateTeam(formValues)
        if (formResult.isSuccess) {
          alert('Team updated successfully!')
          //localStorage.setItem(LocalStorageEnums.teamId, formResult.teamId)
        } else {
          alert('Team update failed')
        }
      } else {
        const formResult = await DefineTeamApiHelper.createTeam(formValues)
        if (formResult.isSuccess) {
          alert('Team created successfully!')
          localStorage.setItem(LocalStorageEnums.teamId, formResult.teamId)
        } else {
          alert('Team creation failed')
        }
      }

      // Add submission logic here
    },
    storeFormRefs({ resetForm, setFieldValue, resetField, setValues, values }) {
      this.resetFormRef = resetForm
      this.setFieldValueRef = setFieldValue
      this.resetFieldRef = resetField
      this.setValuesRef = setValues
      this.valuesRef = values
    },
    async setCurrentTeam(team){
      this.currentTeam = team
    },
    async setIsTeamReadOnly(isTeamReadOnly){
      this.isTeamReadOnly = isTeamReadOnly
    },
    async fetchTeam() {
      await DefineTeamService.fetchTeam({
        addEmail: this.addEmail,
        selectEmail: this.selectEmail,
        setValuesRef: this.setValuesRef,
        isTeamReadOnly: this.setIsTeamReadOnly,
        currentTeam: this.setCurrentTeam,
        setFieldValueRef: this.setFieldValueRef,
      })
    },
    async debounceSearch(event, index) {
      await DefineTeamService.debounceSearch({
        event,
        index,
        searchTimeout: this.searchTimeout,
        searchResults: this.searchResults,
      })
    },
    async selectEmail(email, userId, index, setFieldValue) {
      this.updateEmailField(index, email)
      setFieldValue(`emails.${index}`, email)
      setFieldValue(`user_ids.${index}`, userId)
      this.searchResults[index] = []
    },
  },
  mounted() {
    Promise.all([this.fetchTeam()])
  },
}
</script>

<style scoped>
.is-invalid {
  border-color: #dc3545;
}
.cursor-pointer {
  cursor: pointer;
}
.hover\:bg-gray-100:hover {
  background-color: #f3f4f6;
}
</style>
