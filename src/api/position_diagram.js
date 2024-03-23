import axios from '@/utils/request'

export function getPatientDataByTime(params) {
  return axios.get('/api/patient_by_time/', params)
}

export function getMaxPatientArea() {
  return axios.get('/api/max_patient_area/')
}

export function getDateRange() {
  return axios.get('/api/date_range/')
}
