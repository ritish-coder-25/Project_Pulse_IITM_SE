import * as yup from 'yup'
export const SignupSchema = yup.object().shape({
  username: yup.string().required(),
  password: yup.string().required(),
  first_name: yup.string().required(),
  last_name: yup.string().required(),
  email: yup.string().email().required(),
})
