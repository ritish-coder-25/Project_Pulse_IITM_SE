<template>
  <div class="container">
    <div class="row mt-5">
      <div class="mx-auto col-6 p-4 shadow-sm rounded bg-light form-container">
        <form @submit.prevent="onSubmit">
          <!-- Team Name Input -->
          <div class="mb-3">
            <label class="form-label" for="team-input">Team Name</label>
            <input
              id="team-input"
              type="text"
              :value="values.team"
              @input="handleTeamChange"
              class="form-control"
              :class="{ 'is-invalid': errors.team }"
              :readonly="isTeamReadOnly"
              placeholder="Enter team name"
            />
            <div class="invalid-feedback" v-if="errors.team">
              {{ errors.team }}
            </div>
          </div>

          <!-- Dynamic Email Dropdowns -->
          <div
            v-for="(field, index) in emailFields"
            :key="field.key"
            class="mb-3"
          >
            <label class="form-label">Email {{ index + 1 }}</label>
            <div class="input-group">
              <select
                :value="field.value"
                @change="e => handleEmailChange(e, index)"
                class="form-select"
                :class="{ 'is-invalid': errors[`emails[${index}]`] }"
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
              <button
                type="button"
                class="btn btn-danger"
                @click="removeEmail(index)"
                v-if="emailFields.length > 1"
              >
                Remove
              </button>
              <div class="invalid-feedback" v-if="errors[`emails[${index}]`]">
                {{ errors[`emails[${index}]`] }}
              </div>
            </div>
            <div class="invalid-feedback d-block" v-if="errors.emails">
              {{ errors.emails }}
            </div>
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
        </form>
      </div>
    </div>
  </div>
</template>

<script>
import { DefineTeamApiHelper } from '@/helpers/ApiHelperFuncs/DefineTeam'
import { ref, onMounted } from 'vue'
import { useForm, useFieldArray } from 'vee-validate'
import { DefineTeamSchema } from '@/YupSchemas'

export default {
  name: 'DefineTeamComponent',
  setup() {
    const emailOptions = ref([])
    const isTeamReadOnly = ref(false)

    // Initialize useForm
    const { handleSubmit, reset, setErrors, errors, values, setValues } =
      useForm({
        validationSchema: DefineTeamSchema,
        initialValues: {
          team: '',
          emails: [''],
        },
      })
    console.log('errors', errors)
    // Initialize useFieldArray for 'emails'
    const { fields: emailFields, push, remove } = useFieldArray('emails')

    const fetchTeam = async () => {
      try {
        const teamData = await DefineTeamApiHelper.fetchTeam()
        if (teamData && teamData.name) {
          //setValues({ ...values, team: teamData.name })
          reset({
            team: teamData.name,
            // Preserve existing emails or set if needed
            emails: values.emails.length > 0 ? values.emails : [''],
          })
          isTeamReadOnly.value = true
        }
      } catch (error) {
        console.error('Error fetching team:', error)
      }
    }

    const fetchEmails = async () => {
      try {
        const emails = await DefineTeamApiHelper.fetchEmails()
        emailOptions.value = emails
      } catch (error) {
        console.error('Error fetching emails:', error)
      }
    }

    // Initialize Data
    const initialize = async () => {
      await Promise.all([fetchTeam(), fetchEmails()])
    }

    onMounted(() => {
      initialize()
    })

    // Add Email Field
    const addEmail = () => {
      push('') // Append an empty string to the emails array
    }

    // Remove Email Field
    const removeEmail = index => {
      remove(index)
    }

    const handleTeamChange = event => {
      //setValue('team', event.target.value)
      setValues({ ...values, team: event.target.value })
    }
    const handleEmailChange = (event, index) => {
      const newEmails = [...values.emails]
      newEmails[index] = event.target.value
      setValues({ ...values, emails: newEmails })
    }

    // Submit Handler
    const onSubmit = handleSubmit(formValues => {
      console.log('Form Submitted:', formValues)
      // Add your submission logic here
    })

    return {
      emailOptions,
      addEmail,
      removeEmail,
      onSubmit,
      errors,
      values,
      emailFields,
      //form: values,
      isTeamReadOnly,
      handleTeamChange,
      handleEmailChange,
    }
  },
}
</script>

<style scoped>
.is-invalid {
  border-color: #dc3545;
}
</style>
