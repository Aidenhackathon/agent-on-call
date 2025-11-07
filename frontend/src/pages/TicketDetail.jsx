import React, { useState, useEffect } from 'react';
import { useParams, useNavigate } from 'react-router-dom';
import {
  Container,
  Typography,
  Box,
  CircularProgress,
  Alert,
  Button,
  Paper,
  Chip,
  Grid,
  TextField,
  Dialog,
  DialogTitle,
  DialogContent,
  DialogActions,
} from '@mui/material';
import ArrowBackIcon from '@mui/icons-material/ArrowBack';
import SmartToyIcon from '@mui/icons-material/SmartToy';
import EditIcon from '@mui/icons-material/Edit';
import DeleteIcon from '@mui/icons-material/Delete';
import SaveIcon from '@mui/icons-material/Save';
import TriageResultCard from '../components/TriageResultCard';
import ActivityLog from '../components/ActivityLog';
import { ticketsAPI } from '../api/api';

const statusColors = {
  open: 'default',
  'in-progress': 'primary',
  resolved: 'success',
  closed: 'default',
};

const priorityColors = {
  P0: 'error',
  P1: 'warning',
  P2: 'info',
  P3: 'success',
};

const TicketDetail = () => {
  const { id } = useParams();
  const navigate = useNavigate();
  const [ticket, setTicket] = useState(null);
  const [loading, setLoading] = useState(true);
  const [triaging, setTriaging] = useState(false);
  const [error, setError] = useState(null);
  const [editingReply, setEditingReply] = useState(false);
  const [replyDraft, setReplyDraft] = useState('');
  const [deleteDialogOpen, setDeleteDialogOpen] = useState(false);
  const [editingTicket, setEditingTicket] = useState(false);
  const [ticketTitle, setTicketTitle] = useState('');
  const [ticketDescription, setTicketDescription] = useState('');
  const [saving, setSaving] = useState(false);

  const fetchTicket = async () => {
    try {
      setLoading(true);
      setError(null);
      const data = await ticketsAPI.getById(id);
      setTicket(data);
      setReplyDraft(data.ai_reply_draft || '');
      setTicketTitle(data.title || '');
      setTicketDescription(data.description || '');
    } catch (err) {
      setError('Failed to load ticket. Please try again.');
      console.error(err);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchTicket();
  }, [id]);

  const handleTriage = async () => {
    try {
      setTriaging(true);
      setError(null);
      await ticketsAPI.triage(id);
      await fetchTicket(); // Refresh ticket data
    } catch (err) {
      setError('AI triage failed, please try again.');
      console.error(err);
    } finally {
      setTriaging(false);
    }
  };

  const handleSaveReply = async () => {
    try {
      await ticketsAPI.update(id, { ai_reply_draft: replyDraft });
      setEditingReply(false);
      await fetchTicket();
    } catch (err) {
      setError('Failed to save reply. Please try again.');
      console.error(err);
    }
  };

  const handleSaveTicket = async () => {
    try {
      setSaving(true);
      setError(null);
      
      // Update the ticket
      await ticketsAPI.update(id, {
        title: ticketTitle,
        description: ticketDescription,
      });
      
      // Automatically trigger triage after update
      setSaving(false);
      setTriaging(true);
      try {
        await ticketsAPI.triage(id);
      } catch (triageErr) {
        console.error('Auto-triage failed:', triageErr);
        // Don't show error for triage failure, just log it
      } finally {
        setTriaging(false);
      }
      
      setEditingTicket(false);
      await fetchTicket();
    } catch (err) {
      setError('Failed to save ticket. Please try again.');
      console.error(err);
      setSaving(false);
    }
  };

  const handleCancelEdit = () => {
    setEditingTicket(false);
    if (ticket) {
      setTicketTitle(ticket.title || '');
      setTicketDescription(ticket.description || '');
    }
  };

  const handleDelete = async () => {
    try {
      await ticketsAPI.delete(id);
      navigate('/');
    } catch (err) {
      setError('Failed to delete ticket. Please try again.');
      console.error(err);
    }
  };

  const formatDate = (dateString) => {
    if (!dateString) return 'N/A';
    try {
      const date = new Date(dateString);
      if (isNaN(date.getTime())) return 'N/A';
      // Format only date (no time)
      return new Intl.DateTimeFormat('en-IN', {
        timeZone: 'Asia/Kolkata',
        year: 'numeric',
        month: '2-digit',
        day: '2-digit'
      }).format(date);
    } catch (error) {
      return 'N/A';
    }
  };

  if (loading) {
    return (
      <Box sx={{ display: 'flex', justifyContent: 'center', mt: 5 }}>
        <CircularProgress />
      </Box>
    );
  }

  if (!ticket) {
    return (
      <Container maxWidth="lg">
        <Alert severity="error">Ticket not found</Alert>
      </Container>
    );
  }

  return (
    <Container maxWidth="lg">
      <Box sx={{ mb: 3 }}>
        <Button startIcon={<ArrowBackIcon />} onClick={() => navigate('/')}>
          Back to Tickets
        </Button>
      </Box>

      {error && (
        <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}

      <Paper sx={{ p: 3, mb: 3 }}>
        <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'start', mb: 2 }}>
          {!editingTicket ? (
            <Typography variant="h4" component="h1">
              {ticket.title}
            </Typography>
          ) : (
            <TextField
              fullWidth
              label="Title"
              value={ticketTitle}
              onChange={(e) => setTicketTitle(e.target.value)}
              sx={{ mr: 2 }}
              required
            />
          )}
          <Box sx={{ display: 'flex', gap: 1 }}>
            {!editingTicket ? (
              <>
                <Button
                  variant="outlined"
                  startIcon={<EditIcon />}
                  onClick={() => setEditingTicket(true)}
                >
                  Edit
                </Button>
                <Button
                  variant="outlined"
                  color="error"
                  startIcon={<DeleteIcon />}
                  onClick={() => setDeleteDialogOpen(true)}
                >
                  Delete
                </Button>
              </>
            ) : (
              <>
                <Button
                  variant="contained"
                  startIcon={<SaveIcon />}
                  onClick={handleSaveTicket}
                  disabled={saving || triaging}
                >
                  Save
                </Button>
                <Button
                  variant="outlined"
                  onClick={handleCancelEdit}
                  disabled={saving || triaging}
                >
                  Cancel
                </Button>
              </>
            )}
          </Box>
        </Box>

        <Box sx={{ display: 'flex', gap: 1, mb: 3 }}>
          <Chip label={ticket.status} color={statusColors[ticket.status]} />
          {ticket.priority && (
            <Chip label={ticket.priority} color={priorityColors[ticket.priority] || 'default'} />
          )}
        </Box>

        <Typography variant="h6" gutterBottom>
          Description
        </Typography>
        {!editingTicket ? (
          <Typography variant="body1" paragraph>
            {ticket.description}
          </Typography>
        ) : (
          <TextField
            fullWidth
            label="Description"
            value={ticketDescription}
            onChange={(e) => setTicketDescription(e.target.value)}
            multiline
            rows={4}
            required
          />
        )}

        <Grid container spacing={2} sx={{ mt: 2 }}>
          <Grid item xs={12} sm={6}>
            <Typography variant="caption" color="text.secondary">
              Created: {formatDate(ticket.created_at)}
            </Typography>
          </Grid>
          <Grid item xs={12} sm={6}>
            <Typography variant="caption" color="text.secondary">
              Updated: {formatDate(ticket.updated_at)}
            </Typography>
          </Grid>
        </Grid>

        {!editingTicket && (
          <Box sx={{ mt: 3 }}>
            <Button
              variant="contained"
              color="primary"
              startIcon={triaging ? <CircularProgress size={20} color="inherit" /> : <SmartToyIcon />}
              onClick={handleTriage}
              disabled={triaging}
              size="large"
            >
              {triaging ? 'Triaging...' : 'Auto-Triage with AI'}
            </Button>
          </Box>
        )}
        {(saving || triaging) && (
          <Box sx={{ mt: 2 }}>
            <Alert severity="info">
              {saving ? 'Saving ticket...' : 'Auto-triaging ticket...'}
            </Alert>
          </Box>
        )}
      </Paper>

      {ticket.priority && (
        <TriageResultCard
          triage={{
            priority: ticket.priority,
            ai_confidence: ticket.ai_confidence,
            assignee: ticket.assignee,
            ai_rationale: ticket.ai_rationale,
            ai_reply_draft: ticket.ai_reply_draft,
          }}
        />
      )}

      {ticket.ai_reply_draft && (
        <Paper sx={{ p: 3, mb: 3 }}>
          <Box sx={{ display: 'flex', justifyContent: 'space-between', alignItems: 'center', mb: 2 }}>
            <Typography variant="h6">Reply Draft</Typography>
            {!editingReply ? (
              <Button startIcon={<EditIcon />} onClick={() => setEditingReply(true)}>
                Edit
              </Button>
            ) : (
              <Box>
                <Button startIcon={<SaveIcon />} onClick={handleSaveReply} sx={{ mr: 1 }}>
                  Save
                </Button>
                <Button onClick={() => {
                  setEditingReply(false);
                  setReplyDraft(ticket.ai_reply_draft);
                }}>
                  Cancel
                </Button>
              </Box>
            )}
          </Box>
          {editingReply ? (
            <TextField
              fullWidth
              multiline
              rows={6}
              value={replyDraft}
              onChange={(e) => setReplyDraft(e.target.value)}
            />
          ) : (
            <Box
              sx={{
                backgroundColor: '#f5f5f5',
                p: 2,
                borderRadius: 1,
              }}
            >
              <Typography variant="body1" sx={{ whiteSpace: 'pre-line' }}>
                {ticket.ai_reply_draft}
              </Typography>
            </Box>
          )}
        </Paper>
      )}

      <ActivityLog activities={ticket.activities} />

      <Dialog open={deleteDialogOpen} onClose={() => setDeleteDialogOpen(false)}>
        <DialogTitle>Delete Ticket</DialogTitle>
        <DialogContent>
          Are you sure you want to delete this ticket? This action cannot be undone.
        </DialogContent>
        <DialogActions>
          <Button onClick={() => setDeleteDialogOpen(false)}>Cancel</Button>
          <Button onClick={handleDelete} color="error" variant="contained">
            Delete
          </Button>
        </DialogActions>
      </Dialog>
    </Container>
  );
};

export default TicketDetail;
