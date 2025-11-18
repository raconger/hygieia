import { useState } from 'react'
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  TextField,
} from '@mui/material'
import MetricChart from '../components/MetricChart'

const metricTypes = [
  { value: 'heart_rate', label: 'Heart Rate' },
  { value: 'hrv', label: 'Heart Rate Variability' },
  { value: 'resting_hr', label: 'Resting Heart Rate' },
  { value: 'sleep_duration', label: 'Sleep Duration' },
  { value: 'steps', label: 'Steps' },
  { value: 'weight', label: 'Weight' },
]

const mockData = Array.from({ length: 30 }, (_, i) => ({
  timestamp: new Date(Date.now() - (29 - i) * 24 * 60 * 60 * 1000).toISOString(),
  value: 60 + Math.random() * 20,
}))

export default function Metrics() {
  const [selectedMetric, setSelectedMetric] = useState('heart_rate')
  const [timeRange, setTimeRange] = useState('30d')

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Metrics Explorer
      </Typography>
      <Typography variant="body1" color="text.secondary" paragraph>
        Explore and analyze your health metrics
      </Typography>

      <Card sx={{ mt: 3 }}>
        <CardContent>
          <Grid container spacing={2}>
            <Grid item xs={12} sm={6} md={4}>
              <FormControl fullWidth>
                <InputLabel>Metric</InputLabel>
                <Select
                  value={selectedMetric}
                  label="Metric"
                  onChange={(e) => setSelectedMetric(e.target.value)}
                >
                  {metricTypes.map((type) => (
                    <MenuItem key={type.value} value={type.value}>
                      {type.label}
                    </MenuItem>
                  ))}
                </Select>
              </FormControl>
            </Grid>

            <Grid item xs={12} sm={6} md={4}>
              <FormControl fullWidth>
                <InputLabel>Time Range</InputLabel>
                <Select
                  value={timeRange}
                  label="Time Range"
                  onChange={(e) => setTimeRange(e.target.value)}
                >
                  <MenuItem value="7d">Last 7 Days</MenuItem>
                  <MenuItem value="30d">Last 30 Days</MenuItem>
                  <MenuItem value="90d">Last 90 Days</MenuItem>
                  <MenuItem value="1y">Last Year</MenuItem>
                </Select>
              </FormControl>
            </Grid>
          </Grid>

          <Box sx={{ mt: 4 }}>
            <MetricChart
              title={metricTypes.find(t => t.value === selectedMetric)?.label || ''}
              data={mockData}
              unit="bpm"
            />
          </Box>

          <Box sx={{ mt: 4 }}>
            <Typography variant="h6" gutterBottom>
              Statistics
            </Typography>
            <Grid container spacing={2}>
              <Grid item xs={6} sm={3}>
                <Box>
                  <Typography variant="caption" color="text.secondary">
                    Mean
                  </Typography>
                  <Typography variant="h6">68.4 bpm</Typography>
                </Box>
              </Grid>
              <Grid item xs={6} sm={3}>
                <Box>
                  <Typography variant="caption" color="text.secondary">
                    Median
                  </Typography>
                  <Typography variant="h6">67.2 bpm</Typography>
                </Box>
              </Grid>
              <Grid item xs={6} sm={3}>
                <Box>
                  <Typography variant="caption" color="text.secondary">
                    Min
                  </Typography>
                  <Typography variant="h6">58.1 bpm</Typography>
                </Box>
              </Grid>
              <Grid item xs={6} sm={3}>
                <Box>
                  <Typography variant="caption" color="text.secondary">
                    Max
                  </Typography>
                  <Typography variant="h6">82.5 bpm</Typography>
                </Box>
              </Grid>
            </Grid>
          </Box>
        </CardContent>
      </Card>
    </Box>
  )
}
