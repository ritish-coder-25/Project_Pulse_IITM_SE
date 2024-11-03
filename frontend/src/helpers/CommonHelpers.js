import { format, intervalToDuration } from 'date-fns'

export const getOnlyDateHelper = dateString => {
  console.log('form data', dateString)
  return format(new Date(dateString), 'EEE, dd MMM yyyy')
}
export const formatDateHelper = dateString => {
  console.log('form data', dateString)
  return format(new Date(dateString), 'HH:mm')
}
export const formatDurationHelper = duration => {
  const { hours, minutes, seconds } = intervalToDuration({
    start: 0,
    end: duration * 1000,
  })
  return `${hours}h ${minutes}m ${seconds}s`
}
