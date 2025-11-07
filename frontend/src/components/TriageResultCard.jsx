import React from 'react';
import {
  Card,
  CardContent,
  Typography,
  Box,
  Chip,
  Divider,
} from '@mui/material';
import CheckCircleIcon from '@mui/icons-material/CheckCircle';
import PriorityHighIcon from '@mui/icons-material/PriorityHigh';
import PersonIcon from '@mui/icons-material/Person';

const priorityColors = {
  P0: 'error',
  P1: 'warning',
  P2: 'info',
  P3: 'success',
};

const TriageResultCard = ({ triage }) => {
  if (!triage || !triage.priority) {
    return null;
  }

  const confidencePercent = Math.round(triage.ai_confidence * 100);

  return (
    <Card sx={{ mb: 3, backgroundColor: '#f9f9f9' }}>
      <CardContent>
        <Typography variant="h6" gutterBottom sx={{ display: 'flex', alignItems: 'center' }}>
          <CheckCircleIcon sx={{ mr: 1, color: 'success.main' }} />
          AI Triage Results
        </Typography>

        <Box sx={{ mt: 2 }}>
          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
            <PriorityHighIcon sx={{ mr: 1 }} />
            <Typography variant="subtitle1" sx={{ mr: 2 }}>
              Priority:
            </Typography>
            <Chip
              label={triage.priority}
              color={priorityColors[triage.priority]}
              size="medium"
            />
            <Typography variant="body2" color="text.secondary" sx={{ ml: 2 }}>
              Confidence: {confidencePercent}%
            </Typography>
          </Box>

          <Box sx={{ display: 'flex', alignItems: 'center', mb: 2 }}>
            <PersonIcon sx={{ mr: 1 }} />
            <Typography variant="subtitle1" sx={{ mr: 2 }}>
              Suggested Assignee:
            </Typography>
            <Chip label={triage.assignee} color="primary" variant="outlined" />
          </Box>

          <Divider sx={{ my: 2 }} />

          <Typography variant="subtitle2" gutterBottom>
            Rationale:
          </Typography>
          <Typography variant="body2" color="text.secondary" paragraph>
            {triage.ai_rationale}
          </Typography>

          <Typography variant="subtitle2" gutterBottom>
            Suggested First Reply:
          </Typography>
          <Box
            sx={{
              backgroundColor: 'white',
              p: 2,
              borderRadius: 1,
              border: '1px solid #e0e0e0',
            }}
          >
            <Typography variant="body2" sx={{ whiteSpace: 'pre-line' }}>
              {triage.ai_reply_draft}
            </Typography>
          </Box>
        </Box>
      </CardContent>
    </Card>
  );
};

export default TriageResultCard;
