import * as yup from 'yup'
export const SearchSchema = yup.object().shape({
  search: yup.string().required().min(3),
})
