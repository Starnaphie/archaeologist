import { useState } from 'react'
import { marked } from 'marked'
import styles from './ReadmeView.module.css'

function buildMarkedWithImageBase(repoOwner, repoName) {
  const renderer = new marked.Renderer()
  renderer.image = ({ href, title, text }) => {
    let src = href
    // Convert relative paths to absolute GitHub raw URLs if we have repo info
    if (repoOwner && repoName && href && !href.startsWith('http') && !href.startsWith('//') && !href.startsWith('data:')) {
      src = `https://raw.githubusercontent.com/${repoOwner}/${repoName}/HEAD/${href.replace(/^\.\//, '')}`
    }
    const titleAttr = title ? ` title="${title}"` : ''
    return `<img src="${src}" alt="${text || ''}"${titleAttr} style="max-width:100%;border-radius:4px;" />`
  }
  return { renderer }
}

export default function ReadmeView({ content, repoOwner }) {
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
  const html = marked.parse(clean, buildMarkedWithImageBase(repoOwner?.owner, repoOwner?.repo_name))

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
