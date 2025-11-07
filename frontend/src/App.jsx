import React from 'react';
import { BrowserRouter as Router, Routes, Route } from 'react-router-dom';
import { ThemeProvider, createTheme } from '@mui/material/styles';
import { Box } from '@mui/material';
import TicketList from './pages/TicketList';
import TicketDetail from './pages/TicketDetail';
import CreateTicket from './pages/CreateTicket';
import Navigation from './components/Navigation';

const theme = createTheme({
  palette: {
    primary: {
      main: '#1976d2',
    },
    secondary: {
      main: '#dc004e',
    },
    background: {
      default: '#f5f5f5',
    },
  },
  typography: {
    fontFamily: 'Roboto, sans-serif',
  },
});

function App() {
  return (
    <ThemeProvider theme={theme}>
      <Router>
        <Box sx={{ display: 'flex', flexDirection: 'column', minHeight: '100vh' }}>
          <Navigation />
          <Box component="main" sx={{ flexGrow: 1, p: 3 }}>
            <Routes>
              <Route path="/" element={<TicketList />} />
              <Route path="/tickets/:id" element={<TicketDetail />} />
              <Route path="/create" element={<CreateTicket />} />
            </Routes>
          </Box>
        </Box>
      </Router>
    </ThemeProvider>
  );
}

export default App;
