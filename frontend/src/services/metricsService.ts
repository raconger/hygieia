import api from './api'

export interface Metric {
  metric_type: string
  value: number
  unit: string
  timestamp: string
  source: string
}

export interface MetricSummary {
  metric_type: string
  count: number
  mean: number
  median: number
  min: number
  max: number
  std: number
  unit: string
}

export const metricsService = {
  async getMetrics(params: {
    metric_type?: string
    source?: string
    start_date?: string
    end_date?: string
    limit?: number
  }): Promise<Metric[]> {
    const { data } = await api.get('/metrics', { params })
    return data
  },

  async getMetricTypes() {
    const { data } = await api.get('/metrics/types')
    return data
  },

  async getMetricSummary(
    metric_type: string,
    params?: {
      start_date?: string
      end_date?: string
    }
  ): Promise<MetricSummary> {
    const { data } = await api.get(`/metrics/summary`, {
      params: { metric_type, ...params },
    })
    return data
  },

  async getLatestMetrics() {
    const { data } = await api.get('/metrics/latest')
    return data
  },

  async createMetric(metric: Omit<Metric, 'timestamp'>) {
    const { data } = await api.post('/metrics', metric)
    return data
  },
}
