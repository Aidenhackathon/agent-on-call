import React from 'react';
import {
  Card,
  CardContent,
  Typography,
} from '@mui/material';
import {
  Timeline,
  TimelineItem,
  TimelineSeparator,
  TimelineConnector,
  TimelineContent,
  TimelineDot,
  TimelineOppositeContent,
} from '@mui/lab';
import CreateIcon from '@mui/icons-material/Create';
import EditIcon from '@mui/icons-material/Edit';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import ErrorIcon from '@mui/icons-material/Error';

const ActivityLog = ({ activities }) => {
  if (!activities || activities.length === 0) {
    return null;
  }

  const getIcon = (action) => {
    switch (action) {
      case 'created':
        return <CreateIcon />;
      case 'updated':
        return <EditIcon />;
      case 'triaged':
        return <SmartToyIcon />;
      case 'triage_failed':
        return <ErrorIcon />;
      default:
        return <EditIcon />;
    }
  };

  const getColor = (action) => {
    switch (action) {
      case 'created':
        return 'success';
      case 'triaged':
        return 'primary';
      case 'triage_failed':
        return 'error';
      default:
        return 'grey';
    }
  };

  const formatDate = (dateString) => {
    // Display IST time directly without timezone conversion
    const date = new Date(dateString);
    return date.toLocaleString('en-IN', { 
      timeZone: 'Asia/Kolkata',
      year: 'numeric',
      month: '2-digit',
      day: '2-digit',
      hour: '2-digit',
      minute: '2-digit',
      second: '2-digit',
      hour12: true
    });
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Activity Log
        </Typography>
        <Timeline position="right">
          {activities.map((activity, index) => (
            <TimelineItem key={index}>
              <TimelineOppositeContent color="text.secondary" sx={{ flex: 0.3 }}>
                <Typography variant="caption">{formatDate(activity.timestamp)}</Typography>
              </TimelineOppositeContent>
              <TimelineSeparator>
                <TimelineDot color={getColor(activity.action)}>
                  {getIcon(activity.action)}
                </TimelineDot>
                {index < activities.length - 1 && <TimelineConnector />}
              </TimelineSeparator>
              <TimelineContent>
                <Typography variant="subtitle2">{activity.action}</Typography>
                <Typography variant="body2" color="text.secondary">
                  {activity.details}
                </Typography>
                <Typography variant="caption" color="text.secondary">
                  by {activity.user}
                </Typography>
              </TimelineContent>
            </TimelineItem>
          ))}
        </Timeline>
      </CardContent>
    </Card>
  );
};

export default ActivityLog;
