import React, { useState } from 'react';

export default function App() {
  const [prompt, setPrompt] = useState('');
  const [output, setOutput] = useState('');

  const streamData = async () => {
    const res = await fetch('/infer', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ prompt }),
    });

    const reader = res.body.getReader();
    const decoder = new TextDecoder();

    while (true) {
      const { done, value } = await reader.read();
      if (done) break;
      setOutput(prev => prev + decoder.decode(value));
    }
  };

  return (
    <div>
      <h1>Streaming AI Client</h1>
      <textarea value={prompt} onChange={e => setPrompt(e.target.value)} />
      <button onClick={streamData}>Run</button>
      <pre>{output}</pre>
    </div>
  );
}
