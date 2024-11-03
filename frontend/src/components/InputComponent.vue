<template>
  <div class="mb-3">
    <label class="form-label" :for="name">{{ label }}</label>
    <input
      class="form-control"
      :type="type"
      :id="name"
      :name="name"
      :value="modelValue"
      @input="handleInput"
      :disabled="disabled"
    />
    <div class="form-text">{{ hint }}</div>
    <div class="form-text text-danger" v-if="errorMessage">{{ errorMessage }}</div>
  </div>
</template>

<script>
import { boolean } from 'yup'

export default {
  data: () => ({
    show: false
  }),
  computed: {
    filled() {
      if (!this.show && this.value) {
        return 'has__content'
      }
      return ''
    },
    has__icon() {
      if (this.icon) {
        return 'input__has__icon'
      }
      return
    },
    focus__border() {
      return {
        'background-color': this.color
      }
    }
  },
  props: {
    modelValue: { type: [String,Number], required: false, default: '' },
    label: { type: String, required: false, default: '' },
    hint: { type: String, required: false, default: '' },
    icon: { type: String, required: false, default: '' },
    placeholder: { type: String, required: false, default: '' },
    color: { type: String, required: false, default: 'indigo' },
    type: { type: String, required: false, default: 'text' },
    name: { type: String, required: true },
    errorMessage: { type: String, required: false },
    disabled: {type:Boolean, required: false, default: false}
  },
  methods: {
    handleInput(event) {
      this.$emit('update:modelValue', event.target.value)
    }
  }
}
</script>
