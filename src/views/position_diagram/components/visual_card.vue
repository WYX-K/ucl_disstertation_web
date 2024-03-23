<template>
  <a-card
    style="width: 800px; height: 750px"
    :bodyStyle="{ padding: '5px' }"
    class="flex justify-center items-center"
  >
    <a-spin size="large" :spinning="isLoading">
      <div class="flex flex-col space-y-px">
        <div class="flex space-x-1">
          <div v-for="area in areas1">
            <div
              class="relative"
              :style="{
                height: `${area.height}px`,
                width: `${area.width}px`,
                background: area.color,
              }"
            >
              <div class="flex items-center flex-wrap space-x-1 space-y-1">
                <div v-for="id in area.id">
                  <button
                    type="button"
                    class="inline-block m-1 w-8 h-8 rounded-full bg-cyan-800 text-white"
                    @click="onPatient(id)"
                  >
                    <span style="font-size: 10px">{{ id }}</span>
                  </button>
                </div>
              </div>

              <p class="absolute bottom-2 left-2 font-semibold">
                {{ area.area_name }}
              </p>
            </div>
          </div>
        </div>
        <div v-for="area in areas2">
          <div class="flex space-y-2">
            <div
              class="relative"
              :style="{
                height: `${area.height}px`,
                width: `${area.width}px`,
                background: area.color,
              }"
            >
              <div class="flex items-center ml-14 space-x-1">
                <div v-for="id in area.id">
                  <button
                    type="button"
                    class="inline-block mt-0.5 w-8 h-8 rounded-full bg-cyan-800 text-white"
                    @click="onPatient(id)"
                  >
                    <span style="font-size: 10px">{{ id }}</span>
                  </button>
                </div>
              </div>

              <p class="absolute bottom-2 left-2 font-semibold">
                {{ area.area_name }}
              </p>
            </div>
          </div>
        </div>
      </div>
    </a-spin>
  </a-card>
</template>

<script setup>
import { ref } from 'vue'
import { areasDataStore } from '@/store/area_data'


defineProps({
  isLoading: Boolean,
})

const areasStore = areasDataStore()
const areas1 = ref([])
const areas2 = ref([])
areasStore.$subscribe(
  (_, states) => {
    areas1.value = states.areas.filter((area) => area.row == 1)
    areas2.value = states.areas.filter((area) => area.row == 2)
  },
  { deep: true }
)

const emits = defineEmits(['clickInfo'])

const onPatient = (id) => {
  emits('clickInfo', { id })
}
</script>
