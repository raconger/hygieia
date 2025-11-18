import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  Chip,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
} from '@mui/material'

const correlations = [
  { metric1: 'Sleep Duration', metric2: 'Next-Day HRV', correlation: 0.72, strength: 'Strong' },
  { metric1: 'Training Load', metric2: 'Resting HR', correlation: -0.65, strength: 'Strong' },
  { metric1: 'Air Quality', metric2: 'Activity Performance', correlation: -0.48, strength: 'Moderate' },
  { metric1: 'Sleep Quality', metric2: 'Stress Level', correlation: -0.54, strength: 'Moderate' },
  { metric1: 'Steps', metric2: 'Sleep Duration', correlation: 0.31, strength: 'Weak' },
]

const insights = [
  {
    title: 'Sleep-Recovery Correlation',
    description: 'Your HRV is 18% higher after nights with >7.5 hours of sleep',
    priority: 'high',
  },
  {
    title: 'Training Load Pattern',
    description: 'Resting HR increases by 6% in weeks with >15% training load increase',
    priority: 'medium',
  },
  {
    title: 'Weather Impact',
    description: 'Activity pace is 4% slower on days with AQI >100',
    priority: 'medium',
  },
  {
    title: 'Recovery Trend',
    description: 'HRV shows weekly cyclical pattern with peaks on Sundays',
    priority: 'low',
  },
]

export default function Analytics() {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Analytics & Insights
      </Typography>
      <Typography variant="body1" color="text.secondary" paragraph>
        Discover correlations and patterns in your health data
      </Typography>

      <Grid container spacing={3} sx={{ mt: 2 }}>
        {/* Insights */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Generated Insights
              </Typography>
              <Grid container spacing={2} sx={{ mt: 1 }}>
                {insights.map((insight, index) => (
                  <Grid item xs={12} md={6} key={index}>
                    <Card variant="outlined">
                      <CardContent>
                        <Box display="flex" justifyContent="space-between" alignItems="center">
                          <Typography variant="subtitle1" fontWeight={500}>
                            {insight.title}
                          </Typography>
                          <Chip
                            label={insight.priority}
                            size="small"
                            color={
                              insight.priority === 'high'
                                ? 'error'
                                : insight.priority === 'medium'
                                ? 'warning'
                                : 'default'
                            }
                          />
                        </Box>
                        <Typography variant="body2" color="text.secondary" sx={{ mt: 1 }}>
                          {insight.description}
                        </Typography>
                      </CardContent>
                    </Card>
                  </Grid>
                ))}
              </Grid>
            </CardContent>
          </Card>
        </Grid>

        {/* Correlations */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Metric Correlations
              </Typography>
              <TableContainer component={Paper} variant="outlined" sx={{ mt: 2 }}>
                <Table>
                  <TableHead>
                    <TableRow>
                      <TableCell>Metric 1</TableCell>
                      <TableCell>Metric 2</TableCell>
                      <TableCell align="right">Correlation</TableCell>
                      <TableCell>Strength</TableCell>
                    </TableRow>
                  </TableHead>
                  <TableBody>
                    {correlations.map((row, index) => (
                      <TableRow key={index}>
                        <TableCell>{row.metric1}</TableCell>
                        <TableCell>{row.metric2}</TableCell>
                        <TableCell align="right">
                          <Chip
                            label={row.correlation.toFixed(2)}
                            size="small"
                            color={Math.abs(row.correlation) > 0.6 ? 'success' : 'default'}
                          />
                        </TableCell>
                        <TableCell>{row.strength}</TableCell>
                      </TableRow>
                    ))}
                  </TableBody>
                </Table>
              </TableContainer>
            </CardContent>
          </Card>
        </Grid>

        {/* Anomalies */}
        <Grid item xs={12}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Recent Anomalies
              </Typography>
              <Box sx={{ mt: 2 }}>
                <Typography variant="body2" color="text.secondary">
                  No significant anomalies detected in the last 7 days
                </Typography>
              </Box>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  )
}
