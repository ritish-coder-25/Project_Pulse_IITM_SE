import * as yup from 'yup'
export const DefineTeamSchema = yup.object({
  team: yup.string().required('Team name is required'),
  emails: yup
    .array()
    .of(
      yup
        .string()
        .required('Email is required')
        .email('Invalid email')
        .test(
          'not-empty',
          'Email cannot be empty',
          value => value?.trim() !== '',
        ),
    )
    .min(5, 'Atleast 5 emails are required')
    .max(9, 'Maximum 9 emails allowed'),
  github_repo_url: yup
    .string()
    .url('Github repo url must be a valid url')
    .required('Github repo url is required'),
  user_ids: yup
    .array()
    .of(yup.number())
    .min(5, 'Atleast 1 user is required')
    .max(9, 'Maximum 9 users allowed'),
})
