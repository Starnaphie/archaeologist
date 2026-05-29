import { useEffect, useId, useRef, useState } from 'react'
import mermaid from 'mermaid'
import styles from './ReportView.module.css'

mermaid.initialize({ startOnLoad: false, theme: 'default', securityLevel: 'loose' })

function MermaidDiagram({ code }) {
  const baseId = useId().replace(/:/g, '_')
  const containerRef = useRef(null)
  const [error, setError] = useState(null)

  useEffect(() => {
    let cancelled = false
    if (!code?.trim()) {
      if (containerRef.current) containerRef.current.innerHTML = ''
      return
    }
    setError(null)
    mermaid
      .render(`mmd_${baseId}_${Date.now()}`, code)
      .then(({ svg }) => {
        if (!cancelled && containerRef.current) containerRef.current.innerHTML = svg
      })
      .catch((err) => {
        if (!cancelled) setError(err.message || String(err))
      })
    return () => {
      cancelled = true
    }
  }, [code, baseId])

  if (error) {
    return (
      <div className={styles.mermaidError}>
        <p>Failed to render diagram: {error}</p>
        <pre>{code}</pre>
      </div>
    )
  }
  return <div ref={containerRef} className={styles.mermaid} />
}

function repoNameFromUrl(url) {
  if (!url) return ''
  try {
    const parts = url.replace(/\.git$/, '').replace(/\/$/, '').split('/')
    return parts[parts.length - 1] || url
  } catch {
    return url
  }
}

export default function ReportView({ report, repoUrl }) {
  const repoName = repoNameFromUrl(repoUrl)
  const modules = report.modules || []
  const incomplete = report.incomplete_features || []
  const graph = report.dependency_graph || ''

  return (
    <article className={styles.report}>
      <header className={styles.head}>
        <h2 className={styles.repoName}>{repoName || 'report'}</h2>
        <p className={styles.oneLiner}>{report.one_liner}</p>
      </header>

      <section className={styles.section}>
        <h3 className={styles.sectionTitle}>Purpose</h3>
        <p className={styles.purpose}>{report.purpose}</p>
      </section>

      <section className={styles.section}>
        <h3 className={styles.sectionTitle}>Modules</h3>
        {modules.length === 0 ? (
          <p className={styles.empty}>No modules summarized.</p>
        ) : (
          <table className={styles.table}>
            <thead>
              <tr>
                <th>Name</th>
                <th>Description</th>
              </tr>
            </thead>
            <tbody>
              {modules.map((m, i) => (
                <tr key={i}>
                  <td className={styles.modName}>{m.name}</td>
                  <td>{m.description}</td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </section>

      <section className={styles.section}>
        <h3 className={styles.sectionTitle}>Dependency graph</h3>
        {graph.trim() ? (
          <MermaidDiagram code={graph} />
        ) : (
          <p className={styles.empty}>No internal dependencies detected.</p>
        )}
      </section>

      <section className={styles.section}>
        <h3 className={styles.sectionTitle}>Unfinished work</h3>
        {incomplete.length === 0 ? (
          <p className={styles.empty}>Nothing flagged.</p>
        ) : (
          <ul className={styles.todoList}>
            {incomplete.map((item, i) => (
              <li key={i}>{item}</li>
            ))}
          </ul>
        )}
      </section>
    </article>
  )
}
