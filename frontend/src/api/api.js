import axios from 'axios';

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000';

const api = axios.create({
  baseURL: API_BASE_URL,
  headers: {
    'Content-Type': 'application/json',
  },
});

// Tickets API
export const ticketsAPI = {
  // Get all tickets
  getAll: async () => {
    const response = await api.get('/tickets');
    return response.data;
  },

  // Get single ticket
  getById: async (id) => {
    const response = await api.get(`/tickets/${id}`);
    return response.data;
  },

  // Create ticket
  create: async (ticketData) => {
    const response = await api.post('/tickets', ticketData);
    return response.data;
  },

  // Update ticket
  update: async (id, ticketData) => {
    const response = await api.put(`/tickets/${id}`, ticketData);
    return response.data;
  },

  // Delete ticket
  delete: async (id) => {
    const response = await api.delete(`/tickets/${id}`);
    return response.data;
  },

  // Triage ticket
  triage: async (id) => {
    const response = await api.post(`/tickets/${id}/triage`);
    return response.data;
  },
};

export default api;
