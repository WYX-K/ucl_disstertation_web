<template>
  <a-spin :spinning="spinning" size="large">
    <div :style="{ height: '640px', width: '1450px' }" ref="sankeychart"></div>
  </a-spin>
</template>

<script setup>
import * as echarts from 'echarts/core'
import { SankeyChart } from 'echarts/charts'
import { CanvasRenderer } from 'echarts/renderers'
import { TitleComponent, TooltipComponent } from 'echarts/components'
import { onMounted, ref } from 'vue'
import { getSankeyDiagramData } from '@/api/sankey_diagram'

echarts.use([SankeyChart, CanvasRenderer, TitleComponent, TooltipComponent])

const spinning = ref(true)
const sankeychart = ref()

onMounted(async () => {
  const res = await getSankeyDiagramData()
  draw_sankey(res.data.res.data, res.data.res.links)
  spinning.value = false
})

const draw_sankey = (data, links) => {
  const myChart = echarts.init(sankeychart.value)
  const option = {
    tooltip: {
      trigger: 'item',
      triggerOn: 'mousemove',
    },
    series: {
      left: 'center',
      width: '92%',
      nodeGap: 16,
      lineStyle: {
        color: 'gradient',
        curveness: 0.5,
      },
      type: 'sankey',
      layout: 'none',
      emphasis: {
        focus: 'adjacency',
      },
      label: {
        color: 'rgba(0,0,0,0.7)',
        fontFamily: 'Arial',
        fontSize: 10,
      },
      data,
      links,
    },
  }

  myChart.setOption(option)
}
</script>
