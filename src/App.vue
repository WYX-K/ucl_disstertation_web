<template>
  <a-layout class="layout">
    <a-layout-header>
      <a-menu
        v-model:selectedKeys="selectedKeys"
        theme="dark"
        mode="horizontal"
        :style="{ lineHeight: '64px' }"
        @click="(e) => router.push({ name: e.key })"
      >
        <a-menu-item
          v-for="route in router.getRoutes().slice(1)"
          :key="route.name"
          >{{ route.name }}</a-menu-item
        >
      </a-menu>
    </a-layout-header>
    <a-layout-content class="ml-5 mt-1 mr-5">
      <div class="flex bg-white p-1 justify-center" style="min-height: 695px">
        <router-view v-slot="{ Component }">
          <keep-alive>
            <component :is="Component" />
          </keep-alive>
        </router-view>
      </div>
    </a-layout-content>
    <a-layout-footer style="text-align: center">
      UCL Disstertation ©2024 Created by Yuxin Wang
    </a-layout-footer>
  </a-layout>
</template>

<script setup>
import { computed } from 'vue'
import { useRouter } from 'vue-router'

const router = useRouter()

const selectedKeys = computed({
  get() {
    return [router.currentRoute.value.name]
  },
  set(value) {
    router.push({ name: value[0] })
  },
})
</script>

<style scoped>
.ant-row-rtl #components-layout-demo-top .logo {
  float: right;
  margin: 16px 0 16px 24px;
}

[data-theme='dark'] .site-layout-content {
  background: #141414;
}
</style>
