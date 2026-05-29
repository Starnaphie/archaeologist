import { useState } from 'react'
import ProgressLog from './ProgressLog.jsx'
import ReportView from './ReportView.jsx'
import styles from './App.module.css'

const BACKEND = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'

export default function App() {
  const [url, setUrl] = useState('')
  const [status, setStatus] = useState('idle')
  const [jobId, setJobId] = useState(null)
  const [progress, setProgress] = useState([])
  const [report, setReport] = useState(null)
  const [error, setError] = useState(null)

  async function onSubmit(e) {
    e.preventDefault()
    if (!url.trim() || status === 'running') return
    setStatus('running')
    setJobId(null)
    setProgress([])
    setReport(null)
    setError(null)

    try {
      const res = await fetch(`${BACKEND}/analyze`, {
        method: 'POST',
        headers: { 'Content-Type': 'application/json', Accept: 'text/event-stream' },
        body: JSON.stringify({ github_url: url.trim() }),
      })
      if (!res.ok || !res.body) throw new Error(`backend responded ${res.status}`)

      const reader = res.body.getReader()
      const decoder = new TextDecoder()
      let buffer = ''

      while (true) {
        const { value, done } = await reader.read()
        if (done) break
        const chunk = decoder.decode(value, { stream: true })
        console.log('[SSE chunk]', JSON.stringify(chunk))
        buffer += chunk
        const blocks = buffer.split('\r\n\r\n')
        buffer = blocks.pop() ?? ''
        for (const block of blocks) {
          if (!block.trim()) continue
          let eventType = null
          for (const line of block.split('\r\n')) {
            if (line.startsWith('event: ')) {
              eventType = line.slice(7).trim()
            } else if (line.startsWith('data: ')) {
              const data = line.slice(6).trim()
              if (eventType === 'job_id') setJobId(data)
              if (eventType === 'progress') setProgress(prev => [...prev, data])
              if (eventType === 'done') setReport(JSON.parse(data))
              eventType = null
            }
          }
        }
      }
      setStatus('done')
    } catch (err) {
      setError(err.message || String(err))
      setStatus('error')
    }
  }

  return (
    <div className={styles.app}>
      <header className={styles.header}>
        <h1>archaeologist</h1>
        <p className={styles.subtitle}>Dig through a GitHub repo.</p>
      </header>

      <form className={styles.form} onSubmit={onSubmit}>
        <input
          className={styles.input}
          type="url"
          placeholder="https://github.com/owner/repo"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          disabled={status === 'running'}
          required
        />
        <button
          className={styles.button}
          type="submit"
          disabled={status === 'running' || !url.trim()}
        >
          {status === 'running' ? 'Analyzing…' : 'Analyze'}
        </button>
      </form>

      {jobId && (
        <p className={styles.jobId}>
          job <code>{jobId}</code>
        </p>
      )}

      {progress.length > 0 && <ProgressLog events={progress} />}

      {error && <p className={styles.error}>error: {error}</p>}

      {report && <ReportView report={report} repoUrl={url} />}
    </div>
  )
}
