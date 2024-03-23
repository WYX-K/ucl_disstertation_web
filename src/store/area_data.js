import { defineStore } from 'pinia'

export const areasDataStore = defineStore({
  id: 'areasDataStore',
  state: () => {
    return {
      areas: [],
    }
  },
  actions: {
    setAreasData(data) {
      this.areas = data
    },
  },
  getters: {
    getAreaData: (state) => state.areas,
    getArea1Data: (state) => state.areas.filter((area) => area.row == 1),
    getArea2Data: (state) => state.areas.filter((area) => area.row == 2),
  },
})
