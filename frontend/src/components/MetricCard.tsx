import { Card, CardContent, Typography, Box, CircularProgress } from '@mui/material'
import { TrendingUp, TrendingDown } from '@mui/icons-material'

interface MetricCardProps {
  title: string
  value: number | string
  unit?: string
  change?: number
  trend?: 'up' | 'down'
  loading?: boolean
  color?: string
}

export default function MetricCard({
  title,
  value,
  unit,
  change,
  trend,
  loading,
  color = 'primary.main',
}: MetricCardProps) {
  if (loading) {
    return (
      <Card>
        <CardContent>
          <Box display="flex" justifyContent="center" alignItems="center" minHeight={120}>
            <CircularProgress />
          </Box>
        </CardContent>
      </Card>
    )
  }

  return (
    <Card>
      <CardContent>
        <Typography color="text.secondary" gutterBottom variant="body2">
          {title}
        </Typography>
        <Box display="flex" alignItems="baseline" gap={1}>
          <Typography variant="h4" component="div" sx={{ color }}>
            {value}
          </Typography>
          {unit && (
            <Typography variant="body1" color="text.secondary">
              {unit}
            </Typography>
          )}
        </Box>
        {change !== undefined && (
          <Box display="flex" alignItems="center" gap={0.5} mt={1}>
            {trend === 'up' ? (
              <TrendingUp fontSize="small" color="success" />
            ) : (
              <TrendingDown fontSize="small" color="error" />
            )}
            <Typography
              variant="body2"
              color={trend === 'up' ? 'success.main' : 'error.main'}
            >
              {Math.abs(change)}%
            </Typography>
            <Typography variant="body2" color="text.secondary">
              from last week
            </Typography>
          </Box>
        )}
      </CardContent>
    </Card>
  )
}
