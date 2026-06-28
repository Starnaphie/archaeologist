import { useState, useRef, useCallback } from 'react'
import ProgressLog from './ProgressLog.jsx'
import styles from './App.module.css'
import { startPipeline, pollStatus } from './api/awsClient.js'

const POLL_INTERVAL_MS = 5000

const STATUS_LABELS = {
  RUNNING: 'Pipeline running…',
  SUCCEEDED: 'Complete!',
  FAILED: 'Pipeline failed',
  TIMED_OUT: 'Pipeline timed out',
  ABORTED: 'Pipeline aborted',
}

export default function SlidesGenerator({ onComplete, repoUrl = '' }) {
  const [topic, setTopic] = useState('')
  const [audience, setAudience] = useState('')
  const [tone, setTone] = useState('professional')
  const [numSlides, setNumSlides] = useState('')
  const [description, setDescription] = useState('')
  const [status, setStatus] = useState('idle')
  const [progressEvents, setProgressEvents] = useState([])
  const [error, setError] = useState(null)
  const [executionArn, setExecutionArn] = useState(null)
  const [downloadUrl, setDownloadUrl] = useState(null)

  const pollTimerRef = useRef(null)

  const stopPolling = useCallback(() => {
    if (pollTimerRef.current) {
      clearInterval(pollTimerRef.current)
      pollTimerRef.current = null
    }
  }, [])

  const addProgress = useCallback((msg) => {
    setProgressEvents((prev) => [...prev, msg])
  }, [])

  async function handleSubmit(e) {
    e.preventDefault()
    if (status === 'running') return

    if (!topic.trim()) {
      setError('Please enter a presentation topic.')
      return
    }

    if (!audience.trim()) {
      setError('Please enter a target audience.')
      return
    }

    setStatus('running')
    setProgressEvents([])
    setError(null)
    setDownloadUrl(null)
    setExecutionArn(null)
    addProgress('Starting pipeline…')

    try {
      const { execution_arn, execution_id } = await startPipeline({
        topic: topic.trim(),
        repoSource: repoUrl,
        description: description.trim(),
        audience: audience.trim(),
        tone,
        numSlides: numSlides ? parseInt(numSlides) : null,
      })

      setExecutionArn(execution_arn)
      addProgress(`Execution started: ${execution_id}`)
      addProgress('Researching repository… (this takes ~90 seconds)')

      pollTimerRef.current = setInterval(async () => {
        try {
          const result = await pollStatus(execution_arn)

          if (result.status === 'RUNNING') {
            addProgress(`Still running… (${new Date().toLocaleTimeString()})`)
          }

          if (result.status === 'SUCCEEDED') {
            stopPolling()
            setDownloadUrl(result.download_url)
            addProgress('Slides generated successfully!')
            setStatus('done')
            onComplete?.({ downloadUrl: result.download_url, topic })
          }

          if (['FAILED', 'TIMED_OUT', 'ABORTED'].includes(result.status)) {
            stopPolling()
            setError(result.error || STATUS_LABELS[result.status])
            addProgress(`Pipeline ${result.status.toLowerCase()}.`)
            setStatus('error')
          }
        } catch (err) {
          addProgress(`Poll error: ${err.message}`)
        }
      }, POLL_INTERVAL_MS)
    } catch (err) {
      stopPolling()
      setError(err.message)
      setStatus('error')
      addProgress(`Error: ${err.message}`)
    }
  }

  function handleReset() {
    stopPolling()
    setTopic('')
    setAudience('')
    setTone('professional')
    setNumSlides('')
    setDescription('')
    setStatus('idle')
    setProgressEvents([])
    setError(null)
    setExecutionArn(null)
    setDownloadUrl(null)
  }

  return (
    <div className={styles.app}>
      {(status === 'idle' || status === 'error') && (
        <form className={styles.form} onSubmit={handleSubmit}>
          <label className={styles.label}>
            Presentation topic
            <input
              type="text"
              placeholder="e.g. How this repo works"
              value={topic}
              onChange={(e) => setTopic(e.target.value)}
              disabled={status === 'running'}
              required
              className={styles.input}
            />
          </label>
          <label className={styles.label}>
            Audience
            <input
              type="text"
              placeholder="e.g. Software engineers new to ML"
              value={audience}
              onChange={(e) => setAudience(e.target.value)}
              disabled={status === 'running'}
              required
              className={styles.input}
            />
          </label>
          <div className={styles.row}>
            <label className={styles.label}>
              Tone
              <select
                value={tone}
                onChange={(e) => setTone(e.target.value)}
                disabled={status === 'running'}
                className={styles.select}
              >
                <option value="professional">Professional</option>
                <option value="casual">Casual</option>
                <option value="academic">Academic</option>
              </select>
            </label>
            <label className={styles.label}>
              Max slides
              <select
                value={numSlides}
                onChange={(e) => setNumSlides(e.target.value)}
                disabled={status === 'running'}
                className={styles.select}
              >
                <option value="">Auto (up to 20)</option>
                <option value="5">5</option>
                <option value="8">8</option>
                <option value="10">10</option>
                <option value="12">12</option>
                <option value="15">15</option>
                <option value="20">20</option>
              </select>
            </label>
          </div>
          <label className={styles.label}>
            Additional context (optional)
            <input
              type="text"
              placeholder="e.g. Focus on the ML pipeline"
              value={description}
              onChange={(e) => setDescription(e.target.value)}
              disabled={status === 'running'}
              className={styles.input}
            />
          </label>
          <button
            className={styles.button}
            type="submit"
            disabled={status === 'running' || !topic.trim() || !audience.trim()}
          >
            {status === 'running' ? 'Generating…' : 'Generate Slides'}
          </button>
        </form>
      )}

      {status === 'running' && (
        <p>Polling every 5 seconds — do not close this tab.</p>
      )}

      {executionArn && (
        <p className={styles.jobId}>
          execution <code>{executionArn}</code>
        </p>
      )}

      {progressEvents.length > 0 && <ProgressLog events={progressEvents} />}

      {error && (
        <div className={styles.errorBox}>
          <p>{error}</p>
          <button type="button" className={styles.resetButton} onClick={handleReset}>
            Try again
          </button>
        </div>
      )}

      {downloadUrl && (
        <div className={styles.downloadBox}>
          <p>Your presentation is ready.</p>
          <a href={downloadUrl} download className={styles.downloadButton}>
            Download .pptx
          </a>
          <p className={styles.expiryNote}>Link expires in 1 hour.</p>
          <button type="button" onClick={handleReset} className={styles.resetButton}>
            Generate another
          </button>
        </div>
      )}
    </div>
  )
}
