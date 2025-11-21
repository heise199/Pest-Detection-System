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

const pestList = [
  'Ants', 'Bees', 'Beetles', 'Caterpillars', 'Earthworms', 
  'Earwigs', 'Grasshoppers', 'Moths', 'Slugs', 'Snails', 
  'Wasps', 'Weevils'
]

const initChart = () => {
  const chart = echarts.init(chartRef.value)
  const option = {
    tooltip: {
      trigger: 'axis',
      backgroundColor: 'rgba(255, 255, 255, 0.95)',
      borderColor: '#dbdbdb',
      textStyle: {
        color: '#262626'
      }
    },
    grid: {
      left: '3%',
      right: '4%',
      bottom: '3%',
      containLabel: true
    },
    xAxis: {
      type: 'category',
      data: ['周一', '周二', '周三', '周四', '周五', '周六', '周日'],
      axisLine: {
        lineStyle: {
          color: '#dbdbdb'
        }
      },
      axisLabel: {
        color: '#8e8e8e'
      }
    },
    yAxis: {
      type: 'value',
      axisLine: {
        lineStyle: {
          color: '#dbdbdb'
        }
      },
      axisLabel: {
        color: '#8e8e8e'
      },
      splitLine: {
        lineStyle: {
          color: '#f0f0f0'
        }
      }
    },
    series: [
      {
        data: [12, 20, 15, 8, 7, 11, 13],
        type: 'line',
        smooth: true,
        lineStyle: {
          color: '#0095f6',
          width: 3
        },
        itemStyle: {
          color: '#0095f6'
        },
        areaStyle: {
          color: {
            type: 'linear',
            x: 0,
            y: 0,
            x2: 0,
            y2: 1,
            colorStops: [
              { offset: 0, color: 'rgba(0, 149, 246, 0.3)' },
              { offset: 1, color: 'rgba(0, 149, 246, 0.05)' }
            ]
          }
        }
      }
    ]
  }
  chart.setOption(option)
}
</script>

<template>
  <div class="home-container">
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon">👥</div>
        <div class="stat-content">
          <div class="stat-label">{{ userStore.isAdmin ? '总用户数' : '系统用户' }}</div>
          <div class="stat-value">{{ userStore.isAdmin ? stats.total_users : '---' }}</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon">🔍</div>
        <div class="stat-content">
          <div class="stat-label">{{ userStore.isAdmin ? '总检测次数' : '我的检测' }}</div>
          <div class="stat-value">{{ userStore.isAdmin ? stats.total_detections : '---' }}</div>
        </div>
      </div>
    </div>

    <div class="chart-card">
      <div class="card-header">
        <h3 class="card-title">检测趋势</h3>
        <span class="card-subtitle">近7天数据</span>
      </div>
      <div ref="chartRef" class="chart-container"></div>
    </div>
    
    <div class="info-card">
      <div class="card-header">
        <h3 class="card-title">系统介绍</h3>
      </div>
      <div class="card-body">
        <p class="info-text">本系统基于 YOLOv8 模型，提供高效的农林害虫检测服务。支持图片上传检测与实时视频流检测。</p>
        <div class="pest-tags">
          <span v-for="pest in pestList" :key="pest" class="pest-tag">{{ pest }}</span>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.home-container {
  max-width: 1200px;
  margin: 0 auto;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
  gap: 20px;
  margin-bottom: 24px;
}

.stat-card {
  background: var(--ins-white);
  border: 1px solid var(--ins-border);
  border-radius: var(--ins-radius);
  padding: 24px;
  display: flex;
  align-items: center;
  gap: 20px;
  transition: all 0.3s ease;
  box-shadow: var(--ins-shadow);
}

.stat-card:hover {
  box-shadow: var(--ins-shadow-hover);
  transform: translateY(-2px);
}

.stat-icon {
  font-size: 48px;
  line-height: 1;
  width: 64px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  border-radius: var(--ins-radius-small);
}

.stat-content {
  flex: 1;
}

.stat-label {
  font-size: 14px;
  color: var(--ins-text-secondary);
  margin-bottom: 8px;
}

.stat-value {
  font-size: 32px;
  font-weight: 700;
  color: var(--ins-text-primary);
  line-height: 1;
}

.chart-card,
.info-card {
  background: var(--ins-white);
  border: 1px solid var(--ins-border);
  border-radius: var(--ins-radius);
  padding: 24px;
  margin-bottom: 24px;
  box-shadow: var(--ins-shadow);
}

.card-header {
  display: flex;
  justify-content: space-between;
  align-items: center;
  margin-bottom: 20px;
  padding-bottom: 16px;
  border-bottom: 1px solid var(--ins-border);
}

.card-title {
  font-size: 20px;
  font-weight: 600;
  margin: 0;
  color: var(--ins-text-primary);
}

.card-subtitle {
  font-size: 14px;
  color: var(--ins-text-secondary);
}

.chart-container {
  height: 400px;
}

.card-body {
  padding-top: 8px;
}

.info-text {
  font-size: 15px;
  line-height: 1.6;
  color: var(--ins-text-primary);
  margin-bottom: 20px;
}

.pest-tags {
  display: flex;
  flex-wrap: wrap;
  gap: 8px;
}

.pest-tag {
  background: var(--ins-bg);
  border: 1px solid var(--ins-border);
  border-radius: 20px;
  padding: 6px 16px;
  font-size: 13px;
  color: var(--ins-text-primary);
  transition: all 0.2s ease;
}

.pest-tag:hover {
  background: rgba(0, 149, 246, 0.1);
  border-color: var(--ins-accent);
  color: var(--ins-accent);
}
</style>

