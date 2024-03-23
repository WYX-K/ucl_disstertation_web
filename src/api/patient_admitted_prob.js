import axios from '@/utils/request'

export function getPatientAdmittedProb(params) {
  return axios.get('/api/patient_admitted_prob/', params)
}
