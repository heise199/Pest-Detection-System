<script setup>
import { ref, onMounted } from 'vue'
import * as echarts from 'echarts'
import api from '@/api/axios'
import { User, InfoFilled, Search, DataLine } from '@element-plus/icons-vue'

const stats = ref({
  total_users: 0,
  total_detections: 0,
  total_pests: 0,
  today_detections: 0
})

const chartRef = ref(null)
const loading = ref(false)

const fetchStats = async () => {
  loading.value = true
  try {
    const res = await api.get('/admin/stats')
    stats.value = {
      ...res.data,
      total_pests: res.data.total_pests || 0,
      today_detections: res.data.today_detections || 0
    }
  } catch (e) {
    console.error('获取统计数据失败:', e)
  } finally {
    loading.value = false
  }
}

onMounted(async () => {
  await fetchStats()
  initChart()
})

const initChart = () => {
  if (!chartRef.value) return
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
  <div class="admin-dashboard">
    <div class="stats-grid">
      <div class="stat-card">
        <div class="stat-icon user">
          <el-icon><User /></el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-label">总用户数</div>
          <div class="stat-value">{{ stats.total_users }}</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon detection">
          <el-icon><Search /></el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-label">总检测次数</div>
          <div class="stat-value">{{ stats.total_detections }}</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon pest">
          <el-icon><InfoFilled /></el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-label">害虫种类</div>
          <div class="stat-value">{{ stats.total_pests }}</div>
        </div>
      </div>
      <div class="stat-card">
        <div class="stat-icon trend">
          <el-icon><DataLine /></el-icon>
        </div>
        <div class="stat-content">
          <div class="stat-label">今日检测</div>
          <div class="stat-value">{{ stats.today_detections }}</div>
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
  </div>
</template>

<style scoped>
.admin-dashboard {
  max-width: 1400px;
  margin: 0 auto;
}

.stats-grid {
  display: grid;
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
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
  width: 64px;
  height: 64px;
  display: flex;
  align-items: center;
  justify-content: center;
  border-radius: var(--ins-radius-small);
  font-size: 28px;
}

.stat-icon.user {
  background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
  color: white;
}

.stat-icon.detection {
  background: linear-gradient(135deg, #f093fb 0%, #f5576c 100%);
  color: white;
}

.stat-icon.pest {
  background: linear-gradient(135deg, #4facfe 0%, #00f2fe 100%);
  color: white;
}

.stat-icon.trend {
  background: linear-gradient(135deg, #43e97b 0%, #38f9d7 100%);
  color: white;
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

.chart-card {
  background: var(--ins-white);
  border: 1px solid var(--ins-border);
  border-radius: var(--ins-radius);
  padding: 24px;
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
</style>

