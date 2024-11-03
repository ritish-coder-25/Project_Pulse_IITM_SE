import { format, compareAsc } from 'date-fns'

export const convertShowCreateFormToDto = form => {
  //console.log("form",form);
  const showCreateObj = {
    name: form.name,
    price: form.price,
    rating: form.rating,
    theatre_id: form.selectedTheatreId,
    tags: [],
    showTimings: [],
  }

  const tagsAcc = form.selectedTags.map(val => {
    return val.tag_id
  })
  console.log('reached till showtim')
  const showTimings = form.dateTimes.map(val => {
    return {
      startDateTime: convertDateToLocalTimeMS(val.startDateTime),
      endDateTime: convertDateToLocalTimeMS(val.endDateTime),
    }
  })
  //"2023-05-30T11:00"
  showCreateObj.tags = tagsAcc
  showCreateObj.showTimings = showTimings
  console.log('reached end')
  return showCreateObj
}

export const applyShowDtoToShowCreateForm = (resp, formData) => {
  formData.name = resp.name
  formData.price = resp.price
  formData.rating = resp.rating
  formData.selectedTheatreId = resp.theatre_parent
  const tags = resp.tags.map(val => {
    return {
      tag_id: val.tags_value.tag_id,
      name: val.tags_value.name,
    }
  })

  const showTimings = resp.show_timings.map(val => {
    console.log(
      'timeformatted',
      format(new Date(val.start_time), "yyyy-MM-dd'T'HH:mm"),
    )
    return {
      startDateTime: format(new Date(val.start_time), "yyyy-MM-dd'T'HH:mm"),
      endDateTime: format(new Date(val.end_time), "yyyy-MM-dd'T'HH:mm"),
    }
  })
  formData.selectedTags = tags
  formData.dateTimes = showTimings
}

export const convertDateToLocalTimeMS = dateStr => {
  return (
    new Date(
      new Date(dateStr).toLocaleString('en-US', { timeZone: 'Asia/Kolkata' }),
    ).getTime() / 1000
  )
}
