export const validateField = async (schema, values, field, formErrors) => {
  try {
    if (
      !values[field] ||
      (Array.isArray(values[field]) && values[field].length === 0)
    ) {
      return { message: '' }
    }
    const errors = await schema.validateAt(field, values)
    formErrors[field] = ''
    return { message: '' }
  } catch (err) {
    formErrors[field] = err.message
    return err
  }
}

export const validate = async (schema, values, errors) => {
  try {
    const newVals = await schema.validate(values, { abortEarly: false })
    return true
  } catch (err) {
    err.inner?.map(errorVal => {
      //console.debug("errorVal",errorVal);
      const { path, message } = errorVal
      if (path.includes('.')) {
        // Extracting the field name and index from the path
        const pathRegex = /^(.+?)\[(\d+)\]\.(.+)$/
        const [, nestedPath, index, fieldName] = path.match(pathRegex)
        const indexVal = errors[nestedPath][index]
        if (indexVal) {
          indexVal[fieldName] = message
        } else {
          errors[nestedPath].push({ [fieldName]: message })
        }
      } else {
        errors[errorVal.path] = message
      }
    })
    return false
  }
}
