<template>
  <a-modal v-model:open="isOpen" title="Patient Infomation" @ok="handleOk">
    <a-skeleton :loading="isLoading" active>
      <div class="flex flex-col text-base">
        <p>
          Patient ID: <span class="font-bold">{{ patientInfo.id }}</span>
        </p>
        <p>
          The probability of admission:
          <span class="font-bold">
            {{ (parseFloat(patientInfo.prob) * 100).toFixed(2) }}%
          </span>
        </p>
        <a-timeline class="mt-10">
          <a-timeline-item>
            <template #dot>
              <PlusCircleOutlined />
            </template>
            <p>
              Pathway:
              <span class="font-bold">{{ patientInfo.Pathway }}</span>
            </p>
            <p>
              Time to ED:
              <span class="font-bold">{{ patientInfo.FirstTimetoED }}</span>
            </p>
          </a-timeline-item>
          <a-timeline-item v-for="(area, index) in patientInfo.areas">
            <template #dot v-if="index == patientInfo.areas.length - 1">
              <SyncOutlined :spin="true" />
            </template>

            <p>
              Area: <span class="font-bold">{{ area.area_name }}</span> Stay
              time: <span class="font-bold">{{ parseInt(area.time) }}</span> min
            </p>
          </a-timeline-item>
        </a-timeline>
      </div>
    </a-skeleton>
  </a-modal>
</template>

<script setup>
import { ref, watch, computed } from 'vue'
import { getPatientAdmittedProb } from '@/api/patient_admitted_prob'
import { runStateStore } from '@/store/run_state'
import { SyncOutlined, PlusCircleOutlined } from '@ant-design/icons-vue'
const props = defineProps({
  clickInfo: Object,
  numClick: Number,
})

const patientInfo = ref({})

const isOpen = ref(false)
const runState = runStateStore()
const isLoading = ref(false)
watch(
  () => props.numClick,
  async (newVal) => {
    if (newVal) {
      isOpen.value = true
      isLoading.value = true
      const res = await getPatientAdmittedProb({
        params: {
          id: props.clickInfo.id,
          run_time_now: runState.run_time,
        },
      })
      patientInfo.value = res.data.res
      // await new Promise((resolve) => setTimeout(resolve, 200))
      isLoading.value = false
    }
  }
)

const handleOk = (e) => {
  isOpen.value = false
}
</script>
