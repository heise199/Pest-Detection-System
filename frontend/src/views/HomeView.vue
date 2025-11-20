<script setup>
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'
import api from '@/api/axios'
import { useUserStore } from '@/stores/user'

const userStore = useUserStore()
const stats = ref({
  total_users: 0,
  total_detections: 0
})

const chartRef = ref(null)

onMounted(async () => {
  if (userStore.isAdmin) {
    try {
      const res = await api.get('/admin/stats')
      stats.value = res.data
    } catch (e) {
      console.error(e)
    }
  } else {
      // For normal users, maybe fetch their own history count?
      // For now, we just leave it as --- or mock
  }

  // Mock data for chart if not admin or just for visual
  initChart()
})

const initChart = () => {
  const chart = echarts.init(chartRef.value)
  const option = {
    title: {
      text: '近7天害虫检测趋势'
    },
    tooltip: {
      trigger: 'axis'
    },
    xAxis: {
      type: 'category',
      data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日']
    },
    yAxis: {
      type: 'value'
    },
    series: [
      {
        data: [12, 20, 15, 8, 7, 11, 13], // Mock data
        type: 'line',
        smooth: true
      }
    ]
  }
  chart.setOption(option)
}
</script>

<template>
  <div class="home-container">
    <el-row :gutter="20">
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header>
            {{ userStore.isAdmin ? '总用户数' : '系统用户' }}
          </template>
          <div class="stat-value">
             {{ userStore.isAdmin ? stats.total_users : '---' }}
          </div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header>
            {{ userStore.isAdmin ? '总检测次数' : '我的检测' }}
          </template>
          <div class="stat-value">
            {{ userStore.isAdmin ? stats.total_detections : '---' }}
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="20" class="mt-20">
      <el-col :span="24">
        <el-card>
          <div ref="chartRef" style="height: 400px;"></div>
        </el-card>
      </el-col>
    </el-row>
    
    <el-row class="mt-20">
        <el-col :span="24">
            <el-card>
                <h3>系统介绍</h3>
                <p>本系统基于 YOLOv8 模型，提供高效的农林害虫检测服务。支持图片上传检测与实时视频流检测。</p>
                <p>目前支持检测的害虫包括：Ants, Bees, Beetles, Caterpillars, Earthworms, Earwigs, Grasshoppers, Moths, Slugs, Snails, Wasps, Weevils。</p>
            </el-card>
        </el-col>
    </el-row>
  </div>
</template>

<style scoped>
.stat-value {
  font-size: 24px;
  font-weight: bold;
  color: #409eff;
}
.mt-20 {
  margin-top: 20px;
}
</style>

