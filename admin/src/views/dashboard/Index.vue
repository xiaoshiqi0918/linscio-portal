<template>
  <div>
    <el-row :gutter="16">
      <el-col :span="8" v-for="s in statCards" :key="s.key">
        <el-card shadow="hover" class="stat-card">
          <div class="stat-card__icon" :style="{ background: s.bg, color: s.color }">{{ s.icon }}</div>
          <div class="stat-card__body">
            <div class="stat-card__value">{{ stats[s.key] }}{{ s.suffix || '' }}</div>
            <div class="stat-card__label">{{ s.label }}</div>
          </div>
        </el-card>
      </el-col>
    </el-row>

    <el-row :gutter="16" style="margin-top: 20px;">
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header>
            <span style="font-weight: 600;">最近注册用户</span>
          </template>
          <el-table :data="recentUsers" size="small" :show-header="false">
            <el-table-column prop="email" />
            <el-table-column width="160">
              <template #default="{ row }">
                <span style="font-size: 12px; color: var(--text-muted);">{{ formatTime(row.created_at) }}</span>
              </template>
            </el-table-column>
            <el-table-column width="80">
              <template #default="{ row }">
                <el-tag :type="row.email_verified ? 'success' : 'info'" size="small">
                  {{ row.email_verified ? '已验证' : '未验证' }}
                </el-tag>
              </template>
            </el-table-column>
          </el-table>
          <div v-if="!recentUsers.length" style="text-align:center;padding:20px;color:var(--text-muted);font-size:13px;">暂无数据</div>
        </el-card>
      </el-col>
      <el-col :span="12">
        <el-card shadow="hover">
          <template #header>
            <span style="font-weight: 600;">最近操作日志</span>
          </template>
          <el-table :data="recentLogs" size="small" :show-header="false">
            <el-table-column prop="action_type" width="140">
              <template #default="{ row }">
                <el-tag size="small" type="info">{{ row.action_type }}</el-tag>
              </template>
            </el-table-column>
            <el-table-column>
              <template #default="{ row }">
                <span style="font-size:12px;color:var(--text-secondary);">{{ row.target_type }} {{ row.target_id }}</span>
              </template>
            </el-table-column>
            <el-table-column width="140">
              <template #default="{ row }">
                <span style="font-size:12px;color:var(--text-muted);">{{ formatTime(row.created_at) }}</span>
              </template>
            </el-table-column>
          </el-table>
          <div v-if="!recentLogs.length" style="text-align:center;padding:20px;color:var(--text-muted);font-size:13px;">暂无数据</div>
        </el-card>
      </el-col>
    </el-row>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { getStatsOverview, getUsers, getAdminLogs } from '@/api'

const stats = ref<Record<string, number>>({
  total_users: 0, active_licenses: 0, expiring_soon: 0,
  monthly_downloads: 0, monthly_specialty_downloads: 0, download_success_rate: 0,
})

const statCards = [
  { key: 'total_users', label: '活跃用户', icon: '👥', bg: '#e1effe', color: '#1a56db' },
  { key: 'active_licenses', label: '有效授权', icon: '🔑', bg: '#d1fae5', color: '#059669' },
  { key: 'expiring_soon', label: '即将到期（30天）', icon: '⏰', bg: '#fef3c7', color: '#d97706' },
  { key: 'monthly_downloads', label: '本月软件下载', icon: '📥', bg: '#e1effe', color: '#1a56db' },
  { key: 'monthly_bundle_downloads', label: '本月组件包下载', icon: '🎨', bg: '#fce7f3', color: '#db2777' },
  { key: 'monthly_specialty_downloads', label: '本月学科包下载', icon: '📚', bg: '#ede9fe', color: '#7c3aed' },
  { key: 'download_success_rate', label: '下载成功率', icon: '✅', bg: '#d1fae5', color: '#059669', suffix: '%' },
]

const recentUsers = ref<any[]>([])
const recentLogs = ref<any[]>([])

function formatTime(iso: string) {
  if (!iso) return ''
  const d = new Date(iso)
  return `${d.getMonth() + 1}/${d.getDate()} ${d.getHours().toString().padStart(2, '0')}:${d.getMinutes().toString().padStart(2, '0')}`
}

onMounted(async () => {
  try {
    const [statsRes, usersRes, logsRes] = await Promise.all([
      getStatsOverview(),
      getUsers({ page: 1, size: 5 }),
      getAdminLogs({ page: 1, size: 5 }),
    ])
    stats.value = statsRes.data
    recentUsers.value = usersRes.data.items
    recentLogs.value = logsRes.data.items
  } catch {}
})
</script>

<style scoped>
.stat-card {
  margin-bottom: 4px;
}
.stat-card :deep(.el-card__body) {
  display: flex;
  align-items: center;
  gap: 16px;
  padding: 20px;
}
.stat-card__icon {
  width: 44px;
  height: 44px;
  border-radius: 10px;
  display: flex;
  align-items: center;
  justify-content: center;
  font-size: 18px;
  flex-shrink: 0;
}
.stat-card__value {
  font-size: 24px;
  font-weight: 700;
  color: var(--text-primary);
  line-height: 1;
}
.stat-card__label {
  font-size: 13px;
  color: var(--text-secondary);
  margin-top: 4px;
}
</style>
