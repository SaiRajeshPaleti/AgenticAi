import React, { useState, useRef } from 'react';
import { streamLLM } from './api';

export default function LLMChat() {
  const [prompt, setPrompt] = useState('');
  const [output, setOutput] = useState('');
  const [loading, setLoading] = useState(false);
  const eventSourceRef = useRef(null);

  const handleStart = () => {
    setOutput('');
    setLoading(true);
    if (eventSourceRef.current) eventSourceRef.current.close();
    eventSourceRef.current = streamLLM(
      prompt,
      (token) => setOutput((prev) => prev + token),
      () => setLoading(false),
      () => setLoading(false)
    );
  };

  return (
    <div style={{ maxWidth: 600, margin: '2rem auto', fontFamily: 'sans-serif' }}>
      <h2>Real-Time LLM Agentic AI (Azure)</h2>
      <input
        value={prompt}
        onChange={e => setPrompt(e.target.value)}
        placeholder="Enter your prompt..."
        style={{ width: '80%', padding: 8, fontSize: 16 }}
        disabled={loading}
      />
      <button onClick={handleStart} style={{ marginLeft: 8, padding: '8px 16px' }} disabled={loading}>
        {loading ? 'Loading...' : 'Send'}
      </button>
      <pre style={{ background: '#f4f4f4', minHeight: 120, marginTop: 24, padding: 16 }}>{output}</pre>
    </div>
  );
}
