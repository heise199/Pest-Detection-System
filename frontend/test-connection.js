// 前后端连接测试工具
// 在浏览器控制台运行此代码来测试连接

console.log('=== 前后端连接测试 ===\n')

// 测试1: 后端直接访问
console.log('1. 测试后端直接访问 (http://127.0.0.1:8000/)...')
fetch('http://127.0.0.1:8000/')
  .then(r => r.json())
  .then(data => {
    console.log('✅ 后端服务正常:', data)
  })
  .catch(err => {
    console.error('❌ 后端服务无法访问:', err.message)
    console.log('   请确保后端服务正在运行: uvicorn backend.main:app --reload')
  })

// 测试2: 前端代理访问
setTimeout(() => {
  console.log('\n2. 测试前端代理 (/api/)...')
  fetch('/api/')
    .then(r => r.json())
    .then(data => {
      console.log('✅ 前端代理正常:', data)
    })
    .catch(err => {
      console.error('❌ 前端代理失败:', err.message)
      console.log('   请检查 vite.config.js 中的 proxy 配置')
    })
}, 1000)

// 测试3: 测试登录接口
setTimeout(() => {
  console.log('\n3. 测试登录接口 (/api/token)...')
  const params = new URLSearchParams()
  params.append('username', 'admin')
  params.append('password', 'admin123')
  
  fetch('/api/token', {
    method: 'POST',
    headers: {
      'Content-Type': 'application/x-www-form-urlencoded'
    },
    body: params
  })
    .then(r => r.json())
    .then(data => {
      if (data.access_token) {
        console.log('✅ 登录接口正常，已获取 token')
      } else {
        console.log('⚠️  登录接口返回:', data)
      }
    })
    .catch(err => {
      console.error('❌ 登录接口失败:', err.message)
    })
}, 2000)

console.log('\n提示: 如果所有测试都失败，请检查:')
console.log('  1. 后端服务是否在 http://127.0.0.1:8000 运行')
console.log('  2. 前端服务是否在 http://localhost:5173 运行')
console.log('  3. 浏览器控制台的 Network 标签查看详细错误')

