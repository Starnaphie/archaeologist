import { useEffect, useRef } from 'react'
import styles from './ProgressLog.module.css'

export default function ProgressLog({ events }) {
  const endRef = useRef(null)

  useEffect(() => {
    endRef.current?.scrollIntoView({ behavior: 'smooth', block: 'end' })
  }, [events.length])

  return (
    <div className={styles.log} role="log" aria-live="polite">
      <ul className={styles.list}>
        {events.map((line, i) => (
          <li key={i} className={styles.item}>
            <span className={styles.bullet}>›</span>
            <span>{line}</span>
          </li>
        ))}
      </ul>
      <div ref={endRef} />
    </div>
  )
}
