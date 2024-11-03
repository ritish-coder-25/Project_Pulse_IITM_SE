import { LocalStorageEnums } from '../enums'
import { mainAxios, BASE_URL } from './ApiHelpers'
import { Axios, HttpStatusCode } from 'axios'

export const createTheatreAxios = async ({ name, place, gps, capacity }) => {
  const resp = await mainAxios.post(
    '/theatre',
    JSON.stringify({
      name,
      place,
      gps,
      capacity,
    }),
  )

  return JSON.parse(resp.data)
}

export const editTheatreAxios = async ({ name, capacity, theatreId }) => {
  const resp = await mainAxios.put(
    `/theatre/${theatreId}`,
    JSON.stringify({
      name,
      capacity,
    }),
  )

  return JSON.parse(resp.data)
}

export const deleteTheatreAxios = async ({ theatreId }) => {
  const resp = await mainAxios.delete(`/theatre/${theatreId}`)

  return JSON.parse(resp.data)
}

export const fetchUsersTheatresAxios = async () => {
  const resp = await mainAxios.get('/userstheatres')
  return JSON.parse(resp.data)
}

export const fetchTheatreAxios = async id => {
  const resp = await mainAxios.get(`/theatre/${id}`)
  return JSON.parse(resp.data)
}

export const fetchTheatreShowsCurrentAxios = async id => {
  const resp = await mainAxios.get(`/current-theatre-shows/${id}`)
  return JSON.parse(resp.data)
}

export const fetchAllTagsAxios = async () => {
  const resp = await mainAxios.get('/tags')
  return JSON.parse(resp.data)
}

export const createShowAxios = async form => {
  const resp = await mainAxios.post('/shows', JSON.stringify(form))
  return JSON.parse(resp.data)
}

export const editShowAxios = async (form, showId) => {
  const resp = await mainAxios.put(`/shows/${showId}`, JSON.stringify(form))
  return JSON.parse(resp.data)
}

export const fetchShowAxios = async showId => {
  const resp = await mainAxios.get(`/shows/${showId}`)
  return JSON.parse(resp.data)
}

export const deleteShowAxios = async showId => {
  const resp = await mainAxios.delete(`/shows/${showId}`)
  return JSON.parse(resp.data)
}

export const createTagAxios = async name => {
  const resp = await mainAxios.post('/tag', JSON.stringify({ name }))
  return JSON.parse(resp.data)
}

export const editTagAxios = async (name, id) => {
  const resp = await mainAxios.put(`/tag/${id}`, JSON.stringify({ name }))
  return JSON.parse(resp.data)
}

export const fetchTagAxios = async id => {
  const resp = await mainAxios.get(`/tag/${id}`)
  return JSON.parse(resp.data)
}

export const deleteTagAxios = async id => {
  const resp = await mainAxios.delete(`/tag/${id}`)
  return JSON.parse(resp.data)
}

export const bookTicketAxios = async (theatreId, showId, showTimingId) => {
  const resp = await mainAxios.post(
    '/ticket',
    JSON.stringify({
      theatre_id: theatreId,
      show_id: showId,
      show_timings_id: showTimingId,
    }),
  )
  return JSON.parse(resp.data)
}

export const getUsersTicketsAxios = async () => {
  const resp = await mainAxios.get('/tickets')
  return JSON.parse(resp.data)
}

export const getAdminAllTheatres = async (skip = 0, limit = 100) => {
  const resp = await mainAxios.get('/admin/all-theatres', {
    params: {
      skip: skip,
      limit: limit,
    },
  })

  return JSON.parse(resp.data)
}

export const downloadCsvReportInit = async theatreId => {
  const resp = await mainAxios.get(`/download-theatre-csv/${theatreId}`, {
    timeout: 45000,
  })

  return resp.data
}

export const allHomeShows = async () => {
  const resp = await mainAxios.get(`/all-home-shows`)

  return JSON.parse(resp.data)
}
