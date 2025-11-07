import React from 'react';
import {
  Card,
  CardContent,
  CardActions,
  Typography,
  Chip,
  Button,
  Box,
} from '@mui/material';
import { useNavigate } from 'react-router-dom';
import VisibilityIcon from '@mui/icons-material/Visibility';

const priorityColors = {
  P0: 'error',
  P1: 'warning',
  P2: 'info',
  P3: 'success',
};

const statusColors = {
  open: 'default',
  'in-progress': 'primary',
  resolved: 'success',
  closed: 'default',
};

const TicketCard = ({ ticket }) => {
  const navigate = useNavigate();

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
    <Card sx={{ height: '100%', display: 'flex', flexDirection: 'column' }}>
      <CardContent sx={{ flexGrow: 1 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', mb: 2 }}>
          <Chip label={ticket.status} color={statusColors[ticket.status]} size="small" />
          {ticket.priority && (
            <Chip label={ticket.priority} color={priorityColors[ticket.priority]} size="small" />
          )}
        </Box>
        
        <Typography variant="h6" component="div" gutterBottom>
          {ticket.title}
        </Typography>
        
        <Typography variant="body2" color="text.secondary" sx={{ mb: 1 }}>
          {ticket.description.length > 100
            ? `${ticket.description.substring(0, 100)}...`
            : ticket.description}
        </Typography>
        
        <Box sx={{ mt: 2 }}>
          {ticket.assignee && (
            <Typography variant="caption" display="block" color="text.secondary">
              Assigned to: {ticket.assignee}
            </Typography>
          )}
          <Typography variant="caption" display="block" color="text.secondary">
            Created: {formatDate(ticket.created_at)}
          </Typography>
        </Box>
      </CardContent>
      
      <CardActions>
        <Button
          size="small"
          startIcon={<VisibilityIcon />}
          onClick={() => navigate(`/tickets/${ticket.id}`)}
        >
          View Details
        </Button>
      </CardActions>
    </Card>
  );
};

export default TicketCard;
