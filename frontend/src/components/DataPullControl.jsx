import React, { useState } from 'react';
import { Card, Form, Button, Alert } from 'react-bootstrap';
import api from '../services/api';
import { useAuth } from '../context/AuthContext';

const INGESTION_TIMEOUT_MS = 120000;
const SOURCES = [
  { value: 'adzuna', label: 'Adzuna' },
  { value: 'jobicy', label: 'Jobicy' },
  { value: 'serpapi', label: 'SerpAPI' },
  { value: 'all', label: 'All' },
];

const DataPullControl = () => {
  const [source, setSource] = useState('adzuna');
  const [loading, setLoading] = useState(false);
  const [status, setStatus] = useState(null);
  const [results, setResults] = useState([]);
  const [error, setError] = useState(null);
  const { user } = useAuth();

  const devCredentialsEmail = import.meta.env.VITE_DEV_BYPASS_EMAIL;

  const runOne = async (sourceKey) => {
    const { data } = await api.post(
      `/ingestion/${sourceKey}/top-jobs`,
      null,
      { timeout: INGESTION_TIMEOUT_MS }
    );
    return data;
  };

  const handlePull = async () => {
    setError(null);
    setResults([]);
    setLoading(true);
    setStatus('Pulling…');

    if (user.email == devCredentialsEmail) {
      try {
        if (source === 'all') {
          const list = ['adzuna', 'jobicy', 'serpapi'];
          const out = [];
          for (const key of list) {
            setStatus(`Pulling ${key}…`);
            const data = await runOne(key);
            out.push(data);
          }
          setResults(out);
          setStatus(null);
        } else {
          setStatus(`Pulling ${source}…`);
          const data = await runOne(source);
          setResults([data]);
          setStatus(null);
        }
      } catch (err) {
        const message = err.response?.data?.detail || err.message;
        const failedSource = status ? status.replace('Pulling ', '').replace('…', '') : source;
        setError(`${failedSource}: ${message}`);
        setStatus(null);
      } finally {
        setLoading(false);
      }
    } else {
      setError("Action not allowed for non-admin users.");
      setLoading(false);
    }
  };

  return (
    <Card className="shadow-sm">
      <Card.Header className="bg-light">
        <Card.Title as="h6" className="mb-0">Refresh job data</Card.Title>
      </Card.Header>
      <Card.Body>
        <Form.Group className="mb-3">
          <Form.Label>Source</Form.Label>
          <Form.Select
            value={source}
            onChange={(e) => setSource(e.target.value)}
            disabled={loading}
          >
            {SOURCES.map(({ value, label }) => (
              <option key={value} value={value}>{label}</option>
            ))}
          </Form.Select>
        </Form.Group>
        <Button
          variant="primary"
          onClick={handlePull}
          disabled={loading}
        >
          {loading ? (status || 'Fetching…') : 'Fetch latest jobs'}
        </Button>
        {results.length > 0 && (
          <div className="mt-3 small text-success">
            {results.map((r, i) => (
              <div key={i}>{r.source}: {r.inserted} jobs inserted.</div>
            ))}
          </div>
        )}
        {error && (
          <div className="mt-3 small text-danger">{error}</div>
        )}
      </Card.Body>
    </Card>
  );
};

export default DataPullControl;
