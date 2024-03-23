import { defineStore } from 'pinia'

export const runStateStore = defineStore({
  id: 'runStateStore',
  state: () => {
    return {
      run_time: '',
    }
  },
  actions: {
    setRunTime(data) {
      this.run_time = data
    },
  },
})
