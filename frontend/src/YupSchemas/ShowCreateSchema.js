import * as yup from 'yup'
export const ShowCreateSchema = yup.object().shape({
  name: yup.string().required().min(3),
  rating: yup.number().required().min(0).max(10),
  price: yup.string().required().min(2),
  selectedTheatreId: yup.number().required('Please select a theatre'),
  selectedTags: yup
    .array()
    .of(
      yup.object().shape({
        tag_id: yup.number().required(),
        name: yup.string().required(),
      }),
    )
    .min(1)
    .required('You must select at least one tag'),
  dateTimes: yup
    .array()
    .of(
      yup.object().shape({
        startDateTime: yup.date().required(),
        endDateTime: yup
          .date()
          .required()
          .min(
            yup.ref('startDateTime'),
            'End Date & Time must be greater than Start Date & Time',
          ),
      }),
    )
    .required('At least one date-time slot is required')
    .test(
      'time-overlap',
      'Date & Time slots should not overlap',
      function (value) {
        const slots = value.map(slot => ({
          start: new Date(slot.startDateTime).getTime(),
          end: new Date(slot.endDateTime).getTime(),
        }))

        for (let i = 0; i < slots.length - 1; i++) {
          for (let j = i + 1; j < slots.length; j++) {
            if (
              (slots[j].start >= slots[i].start &&
                slots[j].start <= slots[i].end) ||
              (slots[j].end >= slots[i].start &&
                slots[j].end <= slots[i].end) ||
              (slots[j].start <= slots[i].start && slots[j].end >= slots[i].end)
            ) {
              return false
            }
          }
        }
        return true
      },
    ),
})
