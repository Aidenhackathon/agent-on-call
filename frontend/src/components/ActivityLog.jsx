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
    if (!dateString) {
      console.warn('ActivityLog: No timestamp provided for activity');
      return 'N/A';
    }
    
    try {
      // Parse the date string - handle both ISO strings with timezone and without
      let date = new Date(dateString);
      
      // Check if date is valid
      if (isNaN(date.getTime())) {
        console.warn('ActivityLog: Invalid date string:', dateString);
        return dateString || 'N/A'; // Return original string if invalid
      }
      
      // Always format in IST timezone for display
      // The date object stores UTC internally, so we convert to IST for display
      const formatted = new Intl.DateTimeFormat('en-IN', {
        timeZone: 'Asia/Kolkata',
        year: 'numeric',
        month: '2-digit',
        day: '2-digit',
        hour: '2-digit',
        minute: '2-digit',
        second: '2-digit',
        hour12: true
      }).format(date);
      
      return formatted || 'N/A';
    } catch (error) {
      console.error('ActivityLog: Error formatting date:', error, dateString);
      return dateString || 'N/A';
    }
  };

  return (
    <Card>
      <CardContent>
        <Typography variant="h6" gutterBottom>
          Activity Log
        </Typography>
        <Timeline position="right">
          {activities.map((activity, index) => {
            const timestamp = activity?.timestamp || activity?.created_at || null;
            return (
            <TimelineItem key={index}>
              <TimelineOppositeContent color="text.secondary" sx={{ flex: 0.3 }}>
                <Typography variant="caption">{formatDate(timestamp)}</Typography>
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
            );
          })}
        </Timeline>
      </CardContent>
    </Card>
  );
};

export default ActivityLog;
