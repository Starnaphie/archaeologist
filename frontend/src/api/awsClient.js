const API_BASE = import.meta.env.VITE_AWS_API_URL || ''

export async function startPipeline({
  topic,
  repoSource,
  description = '',
  audience = '',
  tone = 'professional',
  numSlides = null,
}) {
  const body = {
    topic,
    repo_source: repoSource,
    description,
    audience,
    tone,
  }
  if (numSlides !== null) body.num_slides = numSlides

  const response = await fetch(`${API_BASE}/generate`, {
    method: 'POST',
    headers: { 'Content-Type': 'application/json' },
    body: JSON.stringify(body),
  })
  if (!response.ok) {
    const data = await response.json().catch(() => ({}))
    throw new Error(data.error || `HTTP ${response.status}`)
  }
  return response.json()
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
