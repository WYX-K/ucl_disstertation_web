<template>
  <div
    class="block rounded-lg bg-slate-500 p-6 text-lime-50 shadow-secondary-1 h-96 w-96 place-self-center"
  >
    <h5 class="mb-2 text-xl font-medium leading-tight text-center">
      Patient Flow Chart
    </h5>
    <div class="flex flex-col space-y-3">
      <div class="flex flex-col space-y-1">
        <label
          for="email"
          class="block text-sm font-medium leading-6 text-lime-50"
          >Input Search Time:</label
        >
        <a-date-picker
          v-model:value="timeSelected"
          show-time
          @openChange="openChange"
          :disabled-date="disabledDate"
          :showToday="false"
          :showNow="false"
          :allowClear="false"
        />
      </div>
      <div class="flex flex-col space-y-1">
        <div class="block text-sm font-medium leading-6 text-lime-50">
          Running time now:
        </div>
        <a-tag :color="isPaused ? 'error' : 'processing'">
          <template #icon>
            <sync-outlined
              v-if="!isPaused"
              :spin="true"
              :style="{
                position: 'relative',
                bottom: iconoffset ? '3px' : '0px',
              }"
            />
            <minus-circle-outlined
              v-else
              :style="{
                position: 'relative',
                bottom: iconoffset ? '3px' : '0px',
              }"
            />
          </template>
          {{ run_time_now }}
        </a-tag>
      </div>
      <div class="flex flex-row space-x-2">
        <button
          type="button"
          class="inline-block rounded bg-red-400 px-6 pb-2 pt-2.5 text-xs font-medium uppercase leading-normal text-white shadow-primary-3 transition duration-150 ease-in-out hover:bg-red-700 hover:shadow-primary-2 focus:bg-red-700 focus:shadow-primary-2 focus:outline-none focus:ring-0 active:bg-red-500 active:shadow-primary-2"
          data-twe-ripple-init
          data-twe-ripple-color="light"
          @click="onClear"
        >
          Clear
        </button>
        <button
          type="button"
          class="inline-block disabled:opacity-70 rounded disabled:hover:bg-primary-400 bg-primary-400 px-6 pb-2 pt-2.5 text-xs font-medium uppercase leading-normal text-white shadow-primary-3 transition duration-150 ease-in-out hover:bg-primary-700 hover:shadow-primary-2 focus:bg-primary-700 focus:shadow-primary-2 focus:outline-none focus:ring-0 active:bg-primary-500 active:shadow-primary-2"
          data-twe-ripple-init
          data-twe-ripple-color="light"
          @click="onPause"
          :disabled="isLoading"
        >
          {{ isPaused ? 'Start' : 'Pause' }}
        </button>
      </div>
    </div>
  </div>
</template>

<script setup>
import { computed, ref, watch } from 'vue'
import { SyncOutlined, MinusCircleOutlined } from '@ant-design/icons-vue'
import { getPatientDataByTime, getDateRange } from '@/api/position_diagram'
import { areasDataStore } from '@/store/area_data'
import { runStateStore } from '@/store/run_state'
import dayjs from 'dayjs'

const props = defineProps({
  isLoading: Boolean,
  numClick: Number,
})

const iconoffset = ref(true)
const disabledDate = ref()
let time_ticker = ref(0)
let isPaused = ref(true)
let timer = null
const timeSelected = ref(dayjs('2019-06-01 00:00:00'))

const areasState = areasDataStore()
const runState = runStateStore()
const run_time_now = computed(() => {
  if (time_ticker.value == 0) {
    runState.run_time = timeSelected.value
      .add(time_ticker.value * 5, 'minute')
      .format('YYYY-MM-DD HH:mm:ss')
  } else {
    runState.run_time = timeSelected.value
      .add((time_ticker.value - 1) * 5, 'minute')
      .format('YYYY-MM-DD HH:mm:ss')
  }
  return runState.run_time
})

const openChange = async (status) => {
  if (status) {
    let res = await getDateRange()
    res = res.data.res
    timeSelected.value = dayjs(res[0])
    disabledDate.value = (current) => {
      return (
        current < dayjs(res[0]).startOf('day') ||
        current > dayjs(res[1]).endOf('day')
      )
    }
  } else {
    if (
      run_time_now !=
      timeSelected.value
        .add(time_ticker.value * 5, 'minute')
        .format('YYYY-MM-DD HH:mm:ss')
    ) {
      time_ticker.value = 0
      clearTimer()
    }
  }
  clearAreas()
}

watch(
  () => props.numClick,
  (newVal) => {
    if (newVal) {
      isPaused.value = true
      clearTimer()
    }
  }
)
const onPause = (e) => {
  if (!isPaused.value) {
    clearTimer()
    return
  } else {
    isPaused.value = false
  }
  timer = setInterval(async () => {
    let params = {
      n: time_ticker.value,
      start_time: dayjs(timeSelected.value).format('YYYY-MM-DD HH:mm:ss'),
    }
    let res = await getPatientDataByTime({ params })
    res = res.data.res
    if (res.length == 0) {
      time_ticker.value++
      return
    }

    const areas = areasState.getAreaData
    areas.forEach((area) => {
      area.id = area.id.filter((id) => res.includes(id))
      res.forEach((item) => {
        if (area.area_name == item.area_name) {
          if (area.id.includes(item.id)) {
            return
          }
          area.id.push(item.id)
        } else {
          if (area.id.includes(item.id)) {
            area.id = area.id.filter((id) => id != item.id)
          }
        }
      })
    })
    time_ticker.value++
  }, 2000)
}

const onClear = () => {
  time_ticker.value = 0
  timeSelected.value = dayjs('2019-06-01 00:00:00')
  clearTimer()
  clearAreas()
}

const clearTimer = () => {
  if (timer) {
    clearInterval(timer)
  }
  isPaused.value = true
}

const clearAreas = () => {
  const areas = areasState.getAreaData
  areas.forEach((area) => {
    area.id = []
  })
}
</script>
