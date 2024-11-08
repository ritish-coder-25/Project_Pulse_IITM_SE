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
          v-slot="{ values }"
          :validate-on-mount="false"
        >
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

          <!-- Dynamic Email Dropdowns -->
          <div
            v-for="(field, index) in emailFields"
            :key="field.key"
            class="mb-3"
          >
            <label class="form-label">Email {{ index + 1 }}</label>
            <div class="input-group">
              <Field :name="`emails.${index}`" v-slot="{ field, meta }">
                <select
                  v-bind="field"
                  class="form-select"
                  :class="{
                    'is-invalid': meta.touched && meta.errors.length > 0,
                  }"
                >
                  <option value="">Choose...</option>
                  <option
                    v-for="(emailOption, idx) in emailOptions"
                    :key="idx"
                    :value="emailOption"
                  >
                    {{ emailOption }}
                  </option>
                </select>
                <!-- {{ meta }} -->
                <button
                  type="button"
                  class="btn btn-danger"
                  @click="removeEmail(index)"
                  v-if="emailFields.length > 1"
                >
                  Remove
                </button>
                <div class="invalid-feedback">
                  <ErrorMessage
                    :name="`emails[${index}]`"
                    v-if="meta.touched"
                  />
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
              class="btn btn-secondary mb-4 d-block ms-auto"
              @click="addEmail"
            >
              <i class="bi bi-plus-circle me-2"></i>
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

export default {
  name: 'DefineTeamComponent',
  data() {
    return {
      emailOptions: [],
      isTeamReadOnly: false,
      emailFields: [],
      formData: null,
      push: null,
      remove: null,
      reset: null,
      handleSubmit: null,
      errors: null,
      values: null,
    }
  },
  created() {
    // Initialize form
    const { handleSubmit, reset, setErrors, errors, values, setValues } =
      useForm({
        validationSchema: DefineTeamSchema,
        initialValues: {
          team: '',
          emails: [''],
        },
        validateOnMount: false,
        initialTouched: false,
        initialErrors: {},
      })

    // Initialize field array
    const { fields, push, remove } = useFieldArray('emails')

    // Assign to data properties
    this.emailFields = fields
    this.push = push
    this.remove = remove
    this.reset = reset
    this.handleSubmit = handleSubmit
    this.errors = errors
    this.values = values
  },
  methods: {
    resetForm() {
      this.reset()
      this.isTeamReadOnly = false
    },
    addEmail() {
      this.push('')
    },
    removeEmail(index) {
      this.remove(index)
    },
    onSubmit(formValues) {
      console.log('Form Submitted:', formValues)
      // Add submission logic here
    },
    async fetchTeam() {
      try {
        const teamData = await DefineTeamApiHelper.fetchTeam()
        if (teamData && teamData.name) {
          //setValues({ ...values, team: teamData.name })
          this?.reset({
            team: teamData.name,
            // Preserve existing emails or set if needed
            emails: values.emails.length > 0 ? values.emails : [''],
          })
          isTeamReadOnly.value = true
        }
      } catch (error) {
        console.error('Error fetching team:', error)
      }
    },
    async fetchEmails() {
      try {
        const emails = await DefineTeamApiHelper.fetchEmails()
        this.emailOptions = emails
        //this.emailOptions.value = emails
      } catch (error) {
        console.error('Error fetching emails:', error)
      }
    },
  },
  mounted() {
    Promise.all([this.fetchTeam(), this.fetchEmails()])
    // this.fetchTeam()
    // this.fetchEmails()
  },
}
</script>

<style scoped>
.is-invalid {
  border-color: #dc3545;
}
</style>
