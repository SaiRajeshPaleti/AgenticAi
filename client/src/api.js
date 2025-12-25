// API helper for frontend
export function streamLLM(prompt, onToken, onEnd, onError) {
  const url = `http://localhost:5000/stream?prompt=${encodeURIComponent(prompt)}`;
  const es = new EventSource(url);
  es.onmessage = (e) => onToken && onToken(e.data);
  es.onerror = (e) => { es.close(); onError && onError(e); };
  es.onopen = () => {};
  es.addEventListener('end', () => { es.close(); onEnd && onEnd(); });
  return es;
}
