import axios from '@/utils/request'

export function getSankeyDiagramData(params) {
  return axios.get('/api/sankey/', params)
}
