import { Grid, Typography, Box } from '@mui/material'
import MetricCard from '../components/MetricCard'
import MetricChart from '../components/MetricChart'

// Mock data - replace with actual API calls
const mockChartData = [
  { timestamp: '2024-11-11T00:00:00Z', value: 68 },
  { timestamp: '2024-11-12T00:00:00Z', value: 65 },
  { timestamp: '2024-11-13T00:00:00Z', value: 62 },
  { timestamp: '2024-11-14T00:00:00Z', value: 64 },
  { timestamp: '2024-11-15T00:00:00Z', value: 63 },
  { timestamp: '2024-11-16T00:00:00Z', value: 67 },
  { timestamp: '2024-11-17T00:00:00Z', value: 65 },
]

export default function Dashboard() {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Dashboard
      </Typography>
      <Typography variant="body1" color="text.secondary" paragraph>
        Overview of your health metrics
      </Typography>

      <Grid container spacing={3} sx={{ mt: 2 }}>
        {/* Metric Cards */}
        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Resting Heart Rate"
            value={62}
            unit="bpm"
            change={-3.2}
            trend="down"
            color="success.main"
          />
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="HRV"
            value={58}
            unit="ms"
            change={5.1}
            trend="up"
            color="primary.main"
          />
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Sleep Duration"
            value="7h 32m"
            change={-2.1}
            trend="down"
            color="warning.main"
          />
        </Grid>

        <Grid item xs={12} sm={6} md={3}>
          <MetricCard
            title="Daily Steps"
            value="8,542"
            change={12.5}
            trend="up"
            color="success.main"
          />
        </Grid>

        {/* Charts */}
        <Grid item xs={12} md={6}>
          <MetricChart
            title="Resting Heart Rate Trend"
            data={mockChartData}
            unit="bpm"
            color="#2e7d32"
          />
        </Grid>

        <Grid item xs={12} md={6}>
          <MetricChart
            title="HRV Trend"
            data={mockChartData.map(d => ({ ...d, value: d.value - 10 }))}
            unit="ms"
            color="#1976d2"
          />
        </Grid>

        <Grid item xs={12} md={6}>
          <MetricChart
            title="Sleep Duration"
            data={mockChartData.map(d => ({ ...d, value: 7.5 + (Math.random() - 0.5) }))}
            unit="hours"
            color="#9c27b0"
          />
        </Grid>

        <Grid item xs={12} md={6}>
          <MetricChart
            title="Daily Steps"
            data={mockChartData.map(d => ({ ...d, value: 8000 + Math.random() * 4000 }))}
            unit="steps"
            color="#ed6c02"
          />
        </Grid>
      </Grid>
    </Box>
  )
}
