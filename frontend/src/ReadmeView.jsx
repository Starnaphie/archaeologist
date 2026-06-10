import { useState } from 'react'
import { marked } from 'marked'
import styles from './ReadmeView.module.css'

export default function ReadmeView({ content }) {
  const [copied, setCopied] = useState(false)

  async function onCopy() {
    try {
      await navigator.clipboard.writeText(content)
      setCopied(true)
      setTimeout(() => setCopied(false), 1500)
    } catch {
      setCopied(false)
    }
  }

  let clean = content || ''
  if (clean.trimStart().startsWith('```')) {
    clean = clean.split('\n').slice(1).join('\n')
    clean = clean.slice(0, clean.lastIndexOf('```'))
  }
  const html = marked.parse(clean)

  return (
    <div className={styles.wrapper}>
      <div className={styles.panel}>
        <div className={styles.panelHeader}>
          <span className={styles.panelLabel}>Raw</span>
          <button type="button" className={styles.copyButton} onClick={onCopy}>
            {copied ? 'Copied!' : 'Copy'}
          </button>
        </div>
        <textarea
          className={styles.textarea}
          value={content}
          readOnly
        />
      </div>

      <div className={styles.panel}>
        <div className={styles.panelHeader}>
          <span className={styles.panelLabel}>Preview</span>
        </div>
        <div
          className={styles.preview}
          dangerouslySetInnerHTML={{ __html: html }}
        />
      </div>
    </div>
  )
}
