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

export default function SlidesGenerator({ onComplete }) {
  const [topic, setTopic] = useState('')
  const [repoSource, setRepoSource] = useState('')
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
      setError('Presentation topic is required.')
      return
    }

    if (!repoSource.trim()) {
      setError('Repository source is required.')
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
        repoSource: repoSource.trim(),
        description: description.trim(),
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
    setRepoSource('')
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
          <input
            className={styles.input}
            type="text"
            placeholder="Presentation topic e.g. 'How RAG works'"
            value={topic}
            onChange={(e) => setTopic(e.target.value)}
            disabled={status === 'running'}
            required
          />
          <input
            className={styles.input}
            type="url"
            placeholder="https://github.com/owner/repo"
            value={repoSource}
            onChange={(e) => setRepoSource(e.target.value)}
            disabled={status === 'running'}
            required
          />
          <input
            className={styles.input}
            type="text"
            placeholder="Additional context (optional)"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            disabled={status === 'running'}
          />
          <button
            className={styles.button}
            type="submit"
            disabled={status === 'running' || !topic.trim() || !repoSource.trim()}
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
