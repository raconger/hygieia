import { useState } from 'react'
import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  Button,
  Chip,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  IconButton,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
} from '@mui/material'
import {
  Add as AddIcon,
  Edit as EditIcon,
  Delete as DeleteIcon,
  CheckCircle as CheckIcon,
} from '@mui/icons-material'
import { format } from 'date-fns'

const mockAlerts = [
  {
    id: 1,
    title: 'Elevated Resting Heart Rate',
    message: 'Your resting heart rate (68 bpm) is above your normal range (60-65 bpm)',
    priority: 'warning',
    timestamp: new Date(Date.now() - 2 * 60 * 60 * 1000),
    acknowledged: false,
  },
  {
    id: 2,
    title: 'Poor Air Quality',
    message: 'AQI is 125 (Unhealthy for Sensitive Groups). Consider indoor workout.',
    priority: 'info',
    timestamp: new Date(Date.now() - 5 * 60 * 60 * 1000),
    acknowledged: true,
  },
]

const mockRules = [
  {
    id: 1,
    name: 'High Resting HR',
    description: 'Alert when resting HR > 65 bpm',
    type: 'threshold',
    active: true,
  },
  {
    id: 2,
    name: 'Low HRV Trend',
    description: 'Alert when HRV declining for 7 days',
    type: 'trend',
    active: true,
  },
  {
    id: 3,
    name: 'Poor Air Quality',
    description: 'Alert when AQI > 100',
    type: 'environmental',
    active: true,
  },
]

export default function Alerts() {
  const [openDialog, setOpenDialog] = useState(false)

  const handleAcknowledge = (id: number) => {
    // TODO: Implement acknowledge
    console.log('Acknowledge alert', id)
  }

  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Alerts & Notifications
      </Typography>
      <Typography variant="body1" color="text.secondary" paragraph>
        Manage your alert rules and view active alerts
      </Typography>

      <Grid container spacing={3} sx={{ mt: 2 }}>
        {/* Active Alerts */}
        <Grid item xs={12} lg={6}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Active Alerts
              </Typography>
              <List>
                {mockAlerts.map((alert) => (
                  <ListItem
                    key={alert.id}
                    sx={{
                      border: 1,
                      borderColor: 'divider',
                      borderRadius: 1,
                      mb: 1,
                      bgcolor: alert.acknowledged ? 'action.hover' : 'background.paper',
                    }}
                  >
                    <ListItemText
                      primary={
                        <Box display="flex" alignItems="center" gap={1}>
                          <Typography variant="subtitle1">{alert.title}</Typography>
                          <Chip
                            label={alert.priority}
                            size="small"
                            color={
                              alert.priority === 'critical'
                                ? 'error'
                                : alert.priority === 'warning'
                                ? 'warning'
                                : 'info'
                            }
                          />
                        </Box>
                      }
                      secondary={
                        <>
                          <Typography variant="body2" component="span">
                            {alert.message}
                          </Typography>
                          <br />
                          <Typography variant="caption" color="text.secondary">
                            {format(alert.timestamp, 'PPp')}
                          </Typography>
                        </>
                      }
                    />
                    <ListItemSecondaryAction>
                      {!alert.acknowledged && (
                        <IconButton
                          edge="end"
                          onClick={() => handleAcknowledge(alert.id)}
                          color="primary"
                        >
                          <CheckIcon />
                        </IconButton>
                      )}
                    </ListItemSecondaryAction>
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* Alert Rules */}
        <Grid item xs={12} lg={6}>
          <Card>
            <CardContent>
              <Box display="flex" justifyContent="space-between" alignItems="center">
                <Typography variant="h6">Alert Rules</Typography>
                <Button
                  startIcon={<AddIcon />}
                  variant="contained"
                  onClick={() => setOpenDialog(true)}
                >
                  New Rule
                </Button>
              </Box>
              <List sx={{ mt: 2 }}>
                {mockRules.map((rule) => (
                  <ListItem
                    key={rule.id}
                    sx={{
                      border: 1,
                      borderColor: 'divider',
                      borderRadius: 1,
                      mb: 1,
                    }}
                  >
                    <ListItemText
                      primary={
                        <Box display="flex" alignItems="center" gap={1}>
                          <Typography variant="subtitle1">{rule.name}</Typography>
                          <Chip
                            label={rule.active ? 'Active' : 'Inactive'}
                            size="small"
                            color={rule.active ? 'success' : 'default'}
                          />
                        </Box>
                      }
                      secondary={
                        <>
                          <Typography variant="body2">{rule.description}</Typography>
                          <Typography variant="caption" color="text.secondary">
                            Type: {rule.type}
                          </Typography>
                        </>
                      }
                    />
                    <ListItemSecondaryAction>
                      <IconButton edge="end">
                        <EditIcon />
                      </IconButton>
                      <IconButton edge="end">
                        <DeleteIcon />
                      </IconButton>
                    </ListItemSecondaryAction>
                  </ListItem>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>
      </Grid>

      {/* New Rule Dialog */}
      <Dialog open={openDialog} onClose={() => setOpenDialog(false)} maxWidth="sm" fullWidth>
        <DialogTitle>Create Alert Rule</DialogTitle>
        <DialogContent>
          <Box sx={{ mt: 2, display: 'flex', flexDirection: 'column', gap: 2 }}>
            <TextField label="Rule Name" fullWidth />
            <TextField label="Description" fullWidth multiline rows={2} />
            <FormControl fullWidth>
              <InputLabel>Alert Type</InputLabel>
              <Select label="Alert Type" defaultValue="threshold">
                <MenuItem value="threshold">Threshold</MenuItem>
                <MenuItem value="anomaly">Anomaly</MenuItem>
                <MenuItem value="trend">Trend</MenuItem>
                <MenuItem value="environmental">Environmental</MenuItem>
              </Select>
            </FormControl>
            <FormControl fullWidth>
              <InputLabel>Metric</InputLabel>
              <Select label="Metric">
                <MenuItem value="heart_rate">Heart Rate</MenuItem>
                <MenuItem value="hrv">HRV</MenuItem>
                <MenuItem value="sleep_duration">Sleep Duration</MenuItem>
              </Select>
            </FormControl>
            <TextField label="Threshold Value" type="number" fullWidth />
          </Box>
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setOpenDialog(false)}>Cancel</Button>
          <Button variant="contained" onClick={() => setOpenDialog(false)}>
            Create
          </Button>
        </DialogActions>
      </Dialog>
    </Box>
  )
}
