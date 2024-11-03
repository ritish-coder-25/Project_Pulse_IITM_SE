import * as yup from 'yup'
export const TagCreateSchema = yup.object().shape({
  name: yup.string().required().min(3),
})
