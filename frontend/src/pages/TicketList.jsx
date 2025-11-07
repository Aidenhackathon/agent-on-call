import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Grid,
  Box,
  CircularProgress,
  Alert,
  Button,
  Dialog,
  DialogTitle,
  DialogContent,
} from '@mui/material';
import RefreshIcon from '@mui/icons-material/Refresh';
import TicketCard from '../components/TicketCard';
import TicketForm from '../components/TicketForm';
import { ticketsAPI } from '../api/api';

const TicketList = () => {
  const [tickets, setTickets] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [editDialogOpen, setEditDialogOpen] = useState(false);
  const [editingTicket, setEditingTicket] = useState(null);
  const [saving, setSaving] = useState(false);
  const [triaging, setTriaging] = useState(false);
  const navigate = useNavigate();

  const fetchTickets = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await ticketsAPI.getAll();
      setTickets(data);
    } catch (err) {
      setError('Failed to load tickets. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTickets();
  }, []);

  const handleEdit = (ticket) => {
    setEditingTicket(ticket);
    setEditDialogOpen(true);
  };

  const handleEditSubmit = async (formData) => {
    if (!editingTicket) return;
    
    try {
      setSaving(true);
      setError(null);
      
      // Update the ticket
      await ticketsAPI.update(editingTicket.id, formData);
      
      // Automatically trigger triage after update
      setSaving(false);
      setTriaging(true);
      try {
        await ticketsAPI.triage(editingTicket.id);
      } catch (triageErr) {
        console.error('Auto-triage failed:', triageErr);
        // Don't show error for triage failure, just log it
      } finally {
        setTriaging(false);
      }
      
      // Close dialog and refresh tickets
      setEditDialogOpen(false);
      setEditingTicket(null);
      await fetchTickets();
    } catch (err) {
      setError('Failed to update ticket. Please try again.');
      console.error(err);
      setSaving(false);
    }
  };

  const handleEditCancel = () => {
    setEditDialogOpen(false);
    setEditingTicket(null);
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 5 }}>
        <CircularProgress />
      </Box>
    );
  }

  return (
    <Container maxWidth="xl">
      <Box sx={{ mb: 4, display: 'flex', justifyContent: 'space-between', alignItems: 'center' }}>
        <Typography variant="h4" component="h1">
          Helpdesk Tickets
        </Typography>
        <Button
          variant="outlined"
          startIcon={<RefreshIcon />}
          onClick={fetchTickets}
        >
          Refresh
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      {(saving || triaging) && (
        <Alert severity="info" sx={{ mb: 3 }}>
          {saving ? 'Saving ticket...' : 'Auto-triaging ticket...'}
        </Alert>
      )}

      {tickets.length === 0 ? (
        <Alert severity="info">
          No tickets found. Create your first ticket to get started!
        </Alert>
      ) : (
        <Grid container spacing={3}>
          {tickets.map((ticket) => (
            <Grid item xs={12} sm={6} md={4} key={ticket.id}>
              <TicketCard ticket={ticket} onEdit={handleEdit} />
            </Grid>
          ))}
        </Grid>
      )}

      <Dialog 
        open={editDialogOpen} 
        onClose={handleEditCancel}
        maxWidth="md"
        fullWidth
      >
        <DialogTitle>Edit Ticket</DialogTitle>
        <DialogContent>
          {editingTicket && (
            <TicketForm
              initialValues={{
                title: editingTicket.title,
                description: editingTicket.description,
              }}
              onSubmit={handleEditSubmit}
              onCancel={handleEditCancel}
            />
          )}
        </DialogContent>
      </Dialog>
    </Container>
  );
};

export default TicketList;
