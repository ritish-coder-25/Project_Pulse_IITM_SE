import * as yup from 'yup'
export const TicketCreateSchema = yup.object().shape({
  selectedTheatreId: yup.number().required('Please select a theatre'),
  selectedShowId: yup.number().required('Please select shows'),
  selectedShowTimingId: yup.number().required('Please select a show timings'),
})
