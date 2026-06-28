import { useEffect, useId, useRef, useState } from 'react'
import mermaid from 'mermaid'
import { marked } from 'marked'
import styles from './ReportView.module.css'

mermaid.initialize({ startOnLoad: false, theme: 'default', securityLevel: 'loose' })

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

function stripKeyFileLines(md) {
  return md
    .split('\n')
    .filter(line => !line.trim().startsWith('**Key files:**') && !line.trim().startsWith('**Key files: Not found'))
    .join('\n')
}

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

function KeyFilesDropdown({ citations = [], files = [] }) {
  const [open, setOpen] = useState(false)

  // Normalize both citation objects and plain file strings into a unified list
  const items = citations.length > 0
    ? citations.map(c => ({
        label: [c.file_path, c.name, c.kind].filter(Boolean).join(' · '),
        source: c.source || null,
      }))
    : files.map(f => ({ label: f, source: null }))

  if (items.length === 0) return null

  return (
    <div className={styles.citationBlock} style={{ marginTop: 8 }}>
      <button
        className={styles.citationHeader}
        onClick={() => setOpen(o => !o)}
        type="button"
      >
        <span className={styles.citationToggle}>{open ? '▾' : '▸'}</span>
        <span className={styles.citationPath}>key files</span>
        <span className={styles.citationKind}>{items.length} file{items.length !== 1 ? 's' : ''}</span>
      </button>
      {open && (
        <div>
          {items.map((item, i) => (
            <div key={i}>
              <div style={{ padding: '6px 12px', fontFamily: 'var(--mono)', fontSize: 13, color: 'var(--text-h)', borderTop: '1px solid var(--border)' }}>
                {item.label}
              </div>
              {item.source && (
                <pre className={styles.citationSource}>{item.source}</pre>
              )}
            </div>
          ))}
        </div>
      )}
    </div>
  )
}

export default function ReportView({ report, repoUrl }) {
  const repoName = repoNameFromUrl(repoUrl)
  const modules = report.modules || []
  const incomplete = report.incomplete_features || []

  return (
    <article className={styles.report}>
      <header className={styles.head}>
        <h2 className={styles.repoName}>{repoName || 'report'}</h2>
        <p className={styles.oneLiner}>{report.one_liner}</p>
        {report.repo_owner?.owner && (
          <p className={styles.repoOwner}>
            <a href={`https://github.com/${report.repo_owner.owner}/${report.repo_owner.repo_name}`} target="_blank" rel="noopener noreferrer">
              {report.repo_owner.owner}/{report.repo_owner.repo_name}
            </a>
          </p>
        )}
      </header>

      <section className={styles.section}>
        <h3 className={styles.sectionTitle}>Purpose</h3>
        {!report.purpose ? (
          <p className={styles.loading}>Loading…</p>
        ) : (
          <>
            <p className={styles.purpose}>{report.purpose}</p>
            <KeyFilesDropdown citations={report.purpose_citations || []} />
          </>
        )}
      </section>

      <section className={styles.section}>
        <h3 className={styles.sectionTitle}>Modules</h3>
        {!report.modules ? (
          <p className={styles.loading}>Loading…</p>
        ) : modules.length === 0 ? (
          <p className={styles.empty}>No modules summarized.</p>
        ) : (
          <>
            <table className={styles.table}>
              <thead>
                <tr>
                  <th>File</th>
                  <th>Name</th>
                  <th>Description</th>
                </tr>
              </thead>
              <tbody>
                {modules.map((m, i) => (
                  <tr key={i}>
                    <td className={styles.modFile}>{m.file_path || '—'}</td>
                    <td className={styles.modName}>{m.name}</td>
                    <td>{m.description}</td>
                  </tr>
                ))}
              </tbody>
            </table>
            <KeyFilesDropdown citations={report.module_citations || []} />
          </>
        )}
      </section>

      <section className={styles.section}>
        <h3 className={styles.sectionTitle}>Unfinished work</h3>
        {!report.incomplete_features ? (
          <p className={styles.loading}>Loading…</p>
        ) : incomplete.length === 0 ? (
          <p className={styles.empty}>Nothing flagged.</p>
        ) : (
          <>
            <ul className={styles.todoList}>
              {incomplete.map((item, i) => (
                <li key={i}>{item}</li>
              ))}
            </ul>
            <KeyFilesDropdown citations={report.incomplete_citations || []} />
          </>
        )}
      </section>

      <section className={styles.section}>
        <h3 className={styles.sectionTitle}>Repository Structure</h3>
        {!report.folder_hierarchy ? (
          <p className={styles.loading}>Loading…</p>
        ) : report.folder_hierarchy.folders?.length === 0 ? (
          <p className={styles.empty}>No folder structure available.</p>
        ) : (
          <div className={styles.folderList}>
            {(report.folder_hierarchy.folders || []).map((folder, i) => (
              <div key={i} className={styles.folderItem}>
                <span className={styles.folderPath}>{folder.path}/</span>
                <span className={styles.folderDesc}>{folder.description}</span>
              </div>
            ))}
            {(report.folder_hierarchy.root_files || []).map((file, i) => (
              <div key={i} className={styles.folderItem}>
                <span className={styles.folderPath}>{file.path}</span>
                <span className={styles.folderDesc}>{file.description}</span>
              </div>
            ))}
          </div>
        )}
      </section>

      <section className={styles.section}>
        <h3 className={styles.sectionTitle}>Setup</h3>
        {!report.setup_instructions ? (
          <p className={styles.loading}>Loading…</p>
        ) : report.setup_instructions.skipped ? (
          <p className={styles.empty}>No setup files found.</p>
        ) : (
          <>
            <div
              className={styles.setupMarkdown}
              dangerouslySetInnerHTML={{ __html: marked.parse(
                stripKeyFileLines(report.setup_instructions.setup_markdown || ''),
                buildMarkedWithImageBase(report.repo_owner?.owner, report.repo_owner?.repo_name)
              ) }}
            />
            <KeyFilesDropdown files={report.setup_instructions.files_used || []} />
          </>
        )}
      </section>

    </article>
  )
}
