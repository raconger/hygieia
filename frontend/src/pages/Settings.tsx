import {
  Box,
  Typography,
  Card,
  CardContent,
  Grid,
  Button,
  List,
  ListItem,
  ListItemText,
  ListItemSecondaryAction,
  Switch,
  Divider,
  Chip,
} from '@mui/material'
import { Sync as SyncIcon, Check as CheckIcon } from '@mui/icons-material'

const dataSources = [
  { name: 'Garmin Connect', connected: true, lastSync: '2 hours ago' },
  { name: 'Oura Ring', connected: false, lastSync: null },
  { name: 'Strava', connected: true, lastSync: '1 day ago' },
  { name: 'Apple Health', connected: false, lastSync: null },
  { name: 'Wyze Scale', connected: true, lastSync: '3 hours ago' },
]

export default function Settings() {
  return (
    <Box>
      <Typography variant="h4" gutterBottom>
        Settings
      </Typography>
      <Typography variant="body1" color="text.secondary" paragraph>
        Manage your data sources and preferences
      </Typography>

      <Grid container spacing={3} sx={{ mt: 2 }}>
        {/* Data Sources */}
        <Grid item xs={12} lg={8}>
          <Card>
            <CardContent>
              <Box display="flex" justifyContent="space-between" alignItems="center">
                <Typography variant="h6">Data Sources</Typography>
                <Button startIcon={<SyncIcon />} variant="outlined">
                  Sync All
                </Button>
              </Box>
              <List sx={{ mt: 2 }}>
                {dataSources.map((source, index) => (
                  <Box key={source.name}>
                    <ListItem>
                      <ListItemText
                        primary={
                          <Box display="flex" alignItems="center" gap={1}>
                            <Typography variant="subtitle1">{source.name}</Typography>
                            {source.connected && (
                              <Chip
                                label="Connected"
                                size="small"
                                color="success"
                                icon={<CheckIcon />}
                              />
                            )}
                          </Box>
                        }
                        secondary={
                          source.connected
                            ? `Last synced: ${source.lastSync}`
                            : 'Not connected'
                        }
                      />
                      <ListItemSecondaryAction>
                        {source.connected ? (
                          <Button size="small">Disconnect</Button>
                        ) : (
                          <Button size="small" variant="contained">
                            Connect
                          </Button>
                        )}
                      </ListItemSecondaryAction>
                    </ListItem>
                    {index < dataSources.length - 1 && <Divider />}
                  </Box>
                ))}
              </List>
            </CardContent>
          </Card>
        </Grid>

        {/* Preferences */}
        <Grid item xs={12} lg={4}>
          <Card>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Preferences
              </Typography>
              <List>
                <ListItem>
                  <ListItemText
                    primary="Email Notifications"
                    secondary="Receive alerts via email"
                  />
                  <ListItemSecondaryAction>
                    <Switch defaultChecked />
                  </ListItemSecondaryAction>
                </ListItem>
                <Divider />
                <ListItem>
                  <ListItemText
                    primary="Push Notifications"
                    secondary="Receive push notifications"
                  />
                  <ListItemSecondaryAction>
                    <Switch defaultChecked />
                  </ListItemSecondaryAction>
                </ListItem>
                <Divider />
                <ListItem>
                  <ListItemText
                    primary="Auto Sync"
                    secondary="Automatically sync data hourly"
                  />
                  <ListItemSecondaryAction>
                    <Switch defaultChecked />
                  </ListItemSecondaryAction>
                </ListItem>
                <Divider />
                <ListItem>
                  <ListItemText
                    primary="Dark Mode"
                    secondary="Use dark theme"
                  />
                  <ListItemSecondaryAction>
                    <Switch />
                  </ListItemSecondaryAction>
                </ListItem>
              </List>
            </CardContent>
          </Card>

          <Card sx={{ mt: 2 }}>
            <CardContent>
              <Typography variant="h6" gutterBottom>
                Data Retention
              </Typography>
              <Typography variant="body2" color="text.secondary" paragraph>
                Raw data: 365 days
              </Typography>
              <Typography variant="body2" color="text.secondary" paragraph>
                Aggregated data: 5 years
              </Typography>
              <Button variant="outlined" color="error" fullWidth sx={{ mt: 2 }}>
                Export All Data
              </Button>
              <Button variant="outlined" color="error" fullWidth sx={{ mt: 1 }}>
                Delete All Data
              </Button>
            </CardContent>
          </Card>
        </Grid>
      </Grid>
    </Box>
  )
}
