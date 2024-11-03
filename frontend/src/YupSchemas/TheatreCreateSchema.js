import * as yup from 'yup'
export const TheatreCreateSchema = yup.object().shape({
  name: yup.string().required().min(3),
  place: yup.string().required().min(3),
  gps: yup.string().required().min(5),
  capacity: yup.number().min(10).max(1000),
})
