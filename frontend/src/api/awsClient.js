const API_BASE = import.meta.env.VITE_AWS_API_URL || ''

export async function startPipeline({ topic, repoSource, description = '' }) {
  const response = await fetch(`${API_BASE}/generate`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({ topic, repo_source: repoSource, description }),
  })

  const data = await response.json()

  if (!response.ok) {
    throw new Error(data.error || `HTTP ${response.status}`)
  }

  return data
}

export async function pollStatus(executionArn) {
  const response = await fetch(
    `${API_BASE}/status?arn=${encodeURIComponent(executionArn)}`,
  )

  if (!response.ok) {
    throw new Error(`Status check failed: HTTP ${response.status}`)
  }

  return response.json()
}
