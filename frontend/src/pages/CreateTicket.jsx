import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { Container, Alert } from '@mui/material';
import TicketForm from '../components/TicketForm';
import { ticketsAPI } from '../api/api';

const CreateTicket = () => {
  const navigate = useNavigate();
  const [error, setError] = useState(null);

  const handleSubmit = async (formData) => {
    try {
      setError(null);
      const newTicket = await ticketsAPI.create(formData);
      navigate(`/tickets/${newTicket.id}`);
    } catch (err) {
      setError('Failed to create ticket. Please try again.');
      console.error(err);
    }
  };

  return (
    <Container maxWidth="md">
      {error && (
        <Alert severity="error" sx={{ mb: 3 }} onClose={() => setError(null)}>
          {error}
        </Alert>
      )}
      <TicketForm onSubmit={handleSubmit} onCancel={() => navigate('/')} />
    </Container>
  );
};

export default CreateTicket;
