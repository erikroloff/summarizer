import React, { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [selectedFile, setSelectedFile] = useState(null);
  const [summary, setSummary] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleFileChange = (event) => {
    setSelectedFile(event.target.files[0]);
    setSummary('');
    setError('');
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      setError('Please select a PDF file first.');
      return;
    }

    setLoading(true);
    setError('');
    setSummary('');

    const formData = new FormData();
    formData.append('file', selectedFile);

    try {
      const response = await axios.post('http://localhost:8000/summarize-pdf/', formData, {
        headers: {
          'Content-Type': 'multipart/form-data',
          'Access-Control-Allow-Origin': '*',
        },
      });
      setSummary(response.data.summary);
    } catch (err) {
      console.error('Error uploading file:', err);
      setError(err.response?.data?.detail || 'An error occurred during summarization.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="App">
      <header className="App-header">
        <h1>PDF Summarizer</h1>
        <input type="file" accept=".pdf" onChange={handleFileChange} />
        <button onClick={handleUpload} disabled={loading}>
          {loading ? 'Summarizing...' : 'Summarize PDF'}
        </button>
        {error && <p className="error-message">{error}</p>}
        {summary && (
          <div className="summary-container">
            <h2>Summary:</h2>
            <p>{summary}</p>
          </div>
        )}
      </header>
    </div>
  );
}

export default App;