import React from 'react';
import { AppBar, Toolbar, Typography, Button, Box } from '@mui/material';
import { useNavigate, useLocation } from 'react-router-dom';
import SupportAgentIcon from '@mui/icons-material/SupportAgent';
import AddIcon from '@mui/icons-material/Add';
import ListAltIcon from '@mui/icons-material/ListAlt';

const Navigation = () => {
  const navigate = useNavigate();
  const location = useLocation();

  return (
    <AppBar position="static">
      <Toolbar>
        <SupportAgentIcon sx={{ mr: 2 }} />
        <Typography variant="h6" component="div" sx={{ flexGrow: 1 }}>
          Agent-on-Call
        </Typography>
        <Box>
          <Button
            color="inherit"
            startIcon={<ListAltIcon />}
            onClick={() => navigate('/')}
            sx={{
              backgroundColor: location.pathname === '/' ? 'rgba(255,255,255,0.1)' : 'transparent',
            }}
          >
            Tickets
          </Button>
          <Button
            color="inherit"
            startIcon={<AddIcon />}
            onClick={() => navigate('/create')}
            sx={{
              ml: 2,
              backgroundColor: location.pathname === '/create' ? 'rgba(255,255,255,0.1)' : 'transparent',
            }}
          >
            New Ticket
          </Button>
        </Box>
      </Toolbar>
    </AppBar>
  );
};

export default Navigation;
