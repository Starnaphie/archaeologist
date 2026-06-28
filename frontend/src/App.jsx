import { useState } from 'react'
import ProgressLog from './ProgressLog.jsx'
import ReportView from './ReportView.jsx'
import ReadmeView from './ReadmeView.jsx'
import SlidesTab from './SlidesTab.jsx'
import styles from './App.module.css'

// Existing FastAPI backend for Analyze and Generate README modes
const BACKEND = import.meta.env.VITE_BACKEND_URL || 'http://localhost:8000'

export default function App() {
  const [url, setUrl] = useState('')
  const [status, setStatus] = useState('idle')
  const [jobId, setJobId] = useState(null)
  const [analyzeProgress, setAnalyzeProgress] = useState([])
  const [readmeProgress, setReadmeProgress] = useState([])
  const [report, setReport] = useState(null)
  const [readme, setReadme] = useState(null)
  const [error, setError] = useState(null)
  const [generateReadme, setGenerateReadme] = useState(false)
  const [generateSlides, setGenerateSlides] = useState(false)
  const [activeTab, setActiveTab] = useState('analysis')

  async function runAnalysis() {
    let capturedJobId = null
    setReport({})
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
            if (eventType === 'job_id') { setJobId(data); capturedJobId = data }
            if (eventType === 'progress') {
              setAnalyzeProgress(prev => [...prev, data])
            }
            if (eventType === 'section') {
              const sectionData = JSON.parse(data)
              setReport(prev => ({
                ...(prev || {}),
                ...sectionData,
              }))
            }
            if (eventType === 'done') {
              console.log('analysis done event received')
            }
            if (eventType === 'error') throw new Error(data)
            eventType = null
          }
        }
      }
    }
    return capturedJobId
  }

  async function runReadme(resolvedJobId = null) {
    const res = await fetch(`${BACKEND}/generate-readme`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json', Accept: 'text/event-stream' },
      body: JSON.stringify({ github_url: url.trim(), job_id: resolvedJobId }),
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
              setReadmeProgress(prev => [...prev, data])
            }
            if (eventType === 'done') {
              console.log('done event data length:', data.length)
              console.log('done event data first 100 chars:', data.slice(0, 100))
              setReadme(JSON.parse(data).content)
            }
            if (eventType === 'error') throw new Error(data)
            eventType = null
          }
        }
      }
    }
  }

  async function onSubmit(e) {
    e.preventDefault()
    if (!url.trim() || status === 'running') return
    setStatus('running')
    setReadme(null)
    setReadmeProgress([])
    setError(null)
    setActiveTab('analysis')
    // Only reset analysis state if we don't have a prior report
    if (!report || Object.keys(report).length === 0) {
      setJobId(null)
      setReport(null)
      setAnalyzeProgress([])
    }

    try {
      let resolvedJobId = jobId
      // Skip analysis if we already have a report from a prior run
      if (!report || Object.keys(report).length === 0) {
        resolvedJobId = await runAnalysis()
      }

      // Phase 2: auto-run readme if checked.
      if (generateReadme) {
        await runReadme(resolvedJobId)
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
        <div className={styles.checkboxGroup}>
          <label className={styles.checkboxLabel}>
            <input
              type="checkbox"
              checked={generateReadme}
              onChange={(e) => setGenerateReadme(e.target.checked)}
              disabled={status === 'running'}
            />
            Generate README
          </label>
          <label className={styles.checkboxLabel}>
            <input
              type="checkbox"
              checked={generateSlides}
              onChange={(e) => setGenerateSlides(e.target.checked)}
              disabled={status === 'running'}
            />
            Generate Slides
          </label>
        </div>
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
              setGenerateReadme(false)
              setGenerateSlides(false)
              setActiveTab('analysis')
            }}
          >
            Try another repository
          </button>
        </div>
      )}

      {/* Dynamic tabs — only show when there is content to display */}
      {(report || readme || (generateSlides && status === 'done')) && (
        <>
          <div className={styles.tabs}>
            <button
              className={activeTab === 'analysis' ? `${styles.tab} ${styles.tabActive}` : styles.tab}
              onClick={() => setActiveTab('analysis')}
            >
              Analysis
            </button>
            {generateReadme && (readme || status === 'running') && (
              <button
                className={activeTab === 'readme' ? `${styles.tab} ${styles.tabActive}` : styles.tab}
                onClick={() => setActiveTab('readme')}
              >
                README
              </button>
            )}
            {generateSlides && (report || status === 'done') && (
              <button
                className={activeTab === 'slides' ? `${styles.tab} ${styles.tabActive}` : styles.tab}
                onClick={() => setActiveTab('slides')}
              >
                Slides
              </button>
            )}
          </div>

          {/* Analysis tab */}
          <div style={{ display: activeTab === 'analysis' ? 'block' : 'none' }}>
            {analyzeProgress.length > 0 && <ProgressLog events={analyzeProgress} />}
            {report && <ReportView report={report} repoUrl={url} />}
          </div>

          {/* README tab — only if generateReadme was checked */}
          {generateReadme && (
            <div style={{ display: activeTab === 'readme' ? 'block' : 'none' }}>
              {readmeProgress.length > 0 && <ProgressLog events={readmeProgress} />}
              {readme && <ReadmeView content={readme} repoOwner={report?.repo_owner} />}
            </div>
          )}

          {/* Slides tab — only if generateSlides was checked */}
          {generateSlides && (
            <div style={{ display: activeTab === 'slides' ? 'block' : 'none' }}>
              <SlidesTab repoUrl={url} />
            </div>
          )}
        </>
      )}

      {/* Show progress before any results exist */}
      {!report && analyzeProgress.length > 0 && (
        <ProgressLog events={analyzeProgress} />
      )}
    </div>
  )
}
