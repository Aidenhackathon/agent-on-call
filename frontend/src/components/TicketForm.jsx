import React, { useState } from 'react';
import {
  TextField,
  Button,
  Box,
  MenuItem,
  Paper,
  Typography,
} from '@mui/material';

const CATEGORIES = [
  'Technical',
  'Billing',
  'Account',
  'Feature Request',
  'Bug Report',
  'General Inquiry',
  'Critical',
];

const TicketForm = ({ onSubmit, onCancel, initialValues = {} }) => {
  const [formData, setFormData] = useState({
    title: initialValues.title || '',
    description: initialValues.description || '',
    category: initialValues.category || 'Technical',
  });

  const [errors, setErrors] = useState({});

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData((prev) => ({
      ...prev,
      [name]: value,
    }));
    // Clear error for this field
    if (errors[name]) {
      setErrors((prev) => ({
        ...prev,
        [name]: '',
      }));
    }
  };

  const validate = () => {
    const newErrors = {};
    if (!formData.title.trim()) {
      newErrors.title = 'Title is required';
    }
    if (!formData.description.trim()) {
      newErrors.description = 'Description is required';
    }
    if (!formData.category) {
      newErrors.category = 'Category is required';
    }
    setErrors(newErrors);
    return Object.keys(newErrors).length === 0;
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    if (validate()) {
      onSubmit(formData);
    }
  };

  return (
    <Paper sx={{ p: 3 }}>
      <Typography variant="h5" gutterBottom>
        {initialValues.title ? 'Edit Ticket' : 'Create New Ticket'}
      </Typography>
      <Box component="form" onSubmit={handleSubmit} sx={{ mt: 2 }}>
        <TextField
          fullWidth
          label="Title"
          name="title"
          value={formData.title}
          onChange={handleChange}
          error={!!errors.title}
          helperText={errors.title}
          sx={{ mb: 2 }}
          required
        />

        <TextField
          fullWidth
          label="Description"
          name="description"
          value={formData.description}
          onChange={handleChange}
          error={!!errors.description}
          helperText={errors.description}
          multiline
          rows={4}
          sx={{ mb: 2 }}
          required
        />

        <TextField
          fullWidth
          select
          label="Category"
          name="category"
          value={formData.category}
          onChange={handleChange}
          error={!!errors.category}
          helperText={errors.category}
          sx={{ mb: 3 }}
          required
        >
          {CATEGORIES.map((category) => (
            <MenuItem key={category} value={category}>
              {category}
            </MenuItem>
          ))}
        </TextField>

        <Box sx={{ display: 'flex', gap: 2 }}>
          <Button type="submit" variant="contained" color="primary" size="large">
            {initialValues.title ? 'Update' : 'Create'} Ticket
          </Button>
          {onCancel && (
            <Button variant="outlined" onClick={onCancel} size="large">
              Cancel
            </Button>
          )}
        </Box>
      </Box>
    </Paper>
  );
};

export default TicketForm;
