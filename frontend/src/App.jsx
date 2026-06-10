import { useState } from 'react'
import ProgressLog from './ProgressLog.jsx'
import ReportView from './ReportView.jsx'
import ReadmeView from './ReadmeView.jsx'
import styles from './App.module.css'

const BACKEND = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'

export default function App() {
  const [mode, setMode] = useState('Analyze')
  const [url, setUrl] = useState('')
  const [status, setStatus] = useState('idle')
  const [jobId, setJobId] = useState(null)
  const [analyzeProgress, setAnalyzeProgress] = useState([])
  const [readmeProgress, setReadmeProgress] = useState([])
  const [report, setReport] = useState(null)
  const [readme, setReadme] = useState(null)
  const [error, setError] = useState(null)

  function onModeChange(newMode) {
    setMode(newMode)
    setError(null)
    setJobId(null)
    setStatus('idle')
  }

  async function onSubmit(e) {
    e.preventDefault()
    if (!url.trim() || status === 'running') return
    setStatus('running')
    setJobId(null)
    if (mode === 'Generate README') {
      setReadme(null)
      setReadmeProgress([])
    } else {
      setReport(null)
      setAnalyzeProgress([])
    }
    setError(null)

    const endpoint = mode === 'Generate README' ? '/generate-readme' : '/analyze'

    try {
      const res = await fetch(`${BACKEND}${endpoint}`, {
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
              if (eventType === 'progress') {
                mode === 'Generate README'
                  ? setReadmeProgress(prev => [...prev, data])
                  : setAnalyzeProgress(prev => [...prev, data])
              }
              if (eventType === 'done') {
                console.log('done event mode:', mode)
                console.log('done event data length:', data.length)
                console.log('done event data first 100 chars:', data.slice(0, 100))
                if (mode === 'Generate README') {
                  setReadme(JSON.parse(data).content)
                } else {
                  setReport(JSON.parse(data))
                }
              }
              if (eventType === 'error') setError(data)
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

  const currentProgress = mode === 'Generate README'
    ? readmeProgress : analyzeProgress

  return (
    <div className={styles.app}>
      <header className={styles.header}>
        <h1>archaeologist</h1>
        <p className={styles.subtitle}>Dig through a GitHub repo.</p>
      </header>

      <div className={styles.modeToggle}>
        {['Analyze', 'Generate README'].map((m) => (
          <button
            key={m}
            type="button"
            className={mode === m ? styles.modeActive : styles.modeInactive}
            onClick={() => onModeChange(m)}
            disabled={status === 'running'}
          >
            {m}
          </button>
        ))}
      </div>

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
          {status === 'running'
            ? (mode === 'Generate README' ? 'Generating…' : 'Analyzing…')
            : (mode === 'Generate README' ? 'Generate' : 'Analyze')}
        </button>
      </form>

      {jobId && (
        <p className={styles.jobId}>
          job <code>{jobId}</code>
        </p>
      )}

      {error && (
        <div className={styles.errorBox}>
          <p>{error}</p>
          <button
            className={styles.resetButton}
            onClick={() => {
              setUrl('')
              setStatus('idle')
              setJobId(null)
              setAnalyzeProgress([])
              setReadmeProgress([])
              setReport(null)
              setReadme(null)
              setError(null)
            }}
          >
            Try another repository
          </button>
        </div>
      )}

      <div style={{ display: mode === 'Analyze' ? 'block' : 'none' }}>
        {analyzeProgress.length > 0 && <ProgressLog events={analyzeProgress} />}
      </div>
      <div style={{ display: mode === 'Generate README' ? 'block' : 'none' }}>
        {readmeProgress.length > 0 && <ProgressLog events={readmeProgress} />}
      </div>

      <div style={{ display: mode === 'Analyze' ? 'block' : 'none' }}>
        {report && <ReportView report={report} repoUrl={url} />}
      </div>
      <div style={{ display: mode === 'Generate README' ? 'block' : 'none' }}>
        {readme && <ReadmeView content={readme} />}
      </div>
    </div>
  )
}
