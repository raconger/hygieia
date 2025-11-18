import { Box, Typography, Grid, Card, CardContent } from '@mui/material'
import MetricChart from '../components/MetricChart'
import { TrendingUp, TrendingDown, TrendingFlat } from '@mui/icons-material'

const mockData = Array.from({ length: 30 }, (_, i) => ({
  timestamp: new Date(Date.now() - (29 - i) * 24 * 60 * 60 * 1000).toISOString(),
  value: 60 + Math.random() * 20 + i * 0.2,
}))

const TrendCard = ({
  title,
  direction,
  change,
  description,
}: {
  title: string
  direction: 'up' | 'down' | 'flat'
  change: string
  description: string
}) => {
  const icons = {
    up: <TrendingUp sx={{ fontSize: 40 }} color="success" />,
    down: <TrendingDown sx={{ fontSize: 40 }} color="error" />,
    flat: <TrendingFlat sx={{ fontSize: 40 }} color="action" />,
  }

  return (
    <Card>
      <CardContent>
        <Box display="flex" alignItems="center" gap={2}>
          {icons[direction]}
          <Box>
            <Typography variant="h6">{title}</Typography>
            <Typography variant="h4" color={direction === 'up' ? 'success.main' : direction === 'down' ? 'error.main' : 'text.secondary'}>
              {change}
            </Typography>
            <Typography variant="body2" color="text.secondary">
              {description}
            </Typography>
          </Box>
        </Box>
      </CardContent>
    </Card>
  )
}

export default function Trends() {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Trends Analysis
      </Typography>
      <Typography variant="body1" color="text.secondary" paragraph>
        Long-term trends and patterns in your health data
      </Typography>

      <Grid container spacing={3} sx={{ mt: 2 }}>
        <Grid item xs={12} md={4}>
          <TrendCard
            title="HRV Improving"
            direction="up"
            change="+12.5%"
            description="30-day average increase"
          />
        </Grid>

        <Grid item xs={12} md={4}>
          <TrendCard
            title="Resting HR"
            direction="down"
            change="-4.2%"
            description="30-day average decrease"
          />
        </Grid>

        <Grid item xs={12} md={4}>
          <TrendCard
            title="Sleep Duration"
            direction="flat"
            change="0.3%"
            description="Stable over 30 days"
          />
        </Grid>

        <Grid item xs={12} lg={6}>
          <MetricChart
            title="Heart Rate Variability - 90 Day Trend"
            data={mockData}
            unit="ms"
            color="#2e7d32"
          />
        </Grid>

        <Grid item xs={12} lg={6}>
          <MetricChart
            title="Resting Heart Rate - 90 Day Trend"
            data={mockData.map(d => ({ ...d, value: d.value - 5 }))}
            unit="bpm"
            color="#1976d2"
          />
        </Grid>

        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Week-over-Week Comparison
              </Typography>
              <Box sx={{ mt: 2 }}>
                <Grid container spacing={2}>
                  <Grid item xs={6} sm={3}>
                    <Typography variant="caption" color="text.secondary">
                      Current Week Avg HRV
                    </Typography>
                    <Typography variant="h6">58.2 ms</Typography>
                    <Typography variant="body2" color="success.main">
                      +5.1% from last week
                    </Typography>
                  </Grid>
                  <Grid item xs={6} sm={3}>
                    <Typography variant="caption" color="text.secondary">
                      Current Week Avg HR
                    </Typography>
                    <Typography variant="h6">62.4 bpm</Typography>
                    <Typography variant="body2" color="success.main">
                      -3.2% from last week
                    </Typography>
                  </Grid>
                  <Grid item xs={6} sm={3}>
                    <Typography variant="caption" color="text.secondary">
                      Avg Sleep Duration
                    </Typography>
                    <Typography variant="h6">7h 28m</Typography>
                    <Typography variant="body2" color="error.main">
                      -2.1% from last week
                    </Typography>
                  </Grid>
                  <Grid item xs={6} sm={3}>
                    <Typography variant="caption" color="text.secondary">
                      Avg Daily Steps
                    </Typography>
                    <Typography variant="h6">9,124</Typography>
                    <Typography variant="body2" color="success.main">
                      +8.5% from last week
                    </Typography>
                  </Grid>
                </Grid>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  )
}
