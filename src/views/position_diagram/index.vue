<template>
  <div class="flex flex-row space-x-44 items-center">
    <visualCard :isLoading @clickInfo="onclickInfo" />
    <control-card :isLoading :numClick/>
    <patient-info :clickInfo :numClick></patient-info>
  </div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import { getMaxPatientArea } from '@/api/position_diagram'
import controlCard from './components/control_card.vue'
import visualCard from './components/visual_card.vue'
import patientInfo from './components/patient_info.vue'

import { areasDataStore } from '@/store/area_data'
const areasData = areasDataStore()
const isLoading = ref(true)
onMounted(async () => {
  let res = await getMaxPatientArea()
  let areas = res.data.res
  areasData.setAreasData(areas)
  isLoading.value = false
})

const clickInfo = ref({
  id: 0,
})
const numClick = ref(0)
const onclickInfo = (data) => {
  clickInfo.value = data
  numClick.value++
}
</script>
