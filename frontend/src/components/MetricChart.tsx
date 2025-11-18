import { Card, CardContent, Typography, Box } from '@mui/material'
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts'
import { format, parseISO } from 'date-fns'

interface DataPoint {
  timestamp: string
  value: number
  [key: string]: any
}

interface MetricChartProps {
  title: string
  data: DataPoint[]
  dataKey?: string
  color?: string
  unit?: string
}

export default function MetricChart({
  title,
  data,
  dataKey = 'value',
  color = '#1976d2',
  unit,
}: MetricChartProps) {
  const formattedData = data.map((point) => ({
    ...point,
    formattedDate: format(parseISO(point.timestamp), 'MMM dd'),
  }))

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          {title}
        </Typography>
        <Box sx={{ width: '100%', height: 300, mt: 2 }}>
          <ResponsiveContainer>
            <LineChart data={formattedData}>
              <CartesianGrid strokeDasharray="3 3" />
              <XAxis
                dataKey="formattedDate"
                tick={{ fontSize: 12 }}
              />
              <YAxis
                tick={{ fontSize: 12 }}
                label={{
                  value: unit || '',
                  angle: -90,
                  position: 'insideLeft',
                }}
              />
              <Tooltip
                labelFormatter={(label) => `Date: ${label}`}
                formatter={(value: number) => [
                  `${value} ${unit || ''}`,
                  title,
                ]}
              />
              <Legend />
              <Line
                type="monotone"
                dataKey={dataKey}
                stroke={color}
                strokeWidth={2}
                dot={false}
                name={title}
              />
            </LineChart>
          </ResponsiveContainer>
        </Box>
      </CardContent>
    </Card>
  )
}
