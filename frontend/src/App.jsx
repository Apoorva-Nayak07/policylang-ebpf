import { useState } from 'react'
import './App.css'

const DEFAULT_POLICY = `allow ingress
when source.ip == "10.0.0.5"
and destination.port == 443`

const EXAMPLES = [
  {
    name: 'HTTPS Allow',
    policy: `allow ingress
when destination.port == 443`,
  },
  {
    name: 'SSH Deny',
    policy: `deny ingress
when destination.port == 22`,
  },
  {
    name: 'HTTP or HTTPS',
    policy: `allow ingress
when destination.port == 80
or destination.port == 443`,
  },
  {
    name: 'Source IP',
    policy: `allow ingress
when source.ip == "10.0.0.5"`,
  },
]

const STAGES = [
  ['lexer', 'Lexer'],
  ['parser', 'Parser'],
  ['semantic_analysis', 'Semantic Analysis'],
  ['ir_lowering', 'IR Lowering'],
  ['optimization', 'Optimizer'],
  ['ebpf_generation', 'eBPF Generation'],
]

const FIELD_LABELS = {
  SRC_IP: 'Source IP',
  DST_IP: 'Destination IP',
  SRC_PORT: 'Source Port',
  DST_PORT: 'Destination Port',
  PROTOCOL: 'Protocol',
}

const OPERATOR_LABELS = {
  EQ: '==',
  NE: '!=',
}

function App() {
  const [source, setSource] = useState(DEFAULT_POLICY)
  const [loading, setLoading] = useState(false)
  const [result, setResult] = useState(null)
  const [error, setError] = useState('')

  const compilePolicy = async () => {
    setLoading(true)
    setError('')
    setResult(null)

    try {
      const response = await fetch('http://127.0.0.1:5000/compile', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          source,
        }),
      })

      const data = await response.json()

      if (!response.ok || !data.success) {
        throw new Error(data.error || 'Compilation failed')
      }

      setResult(data)
    } catch (err) {
      setError(
        err instanceof Error
          ? err.message
          : 'Unable to connect to the compiler API'
      )
    } finally {
      setLoading(false)
    }
  }

  const copyCode = async () => {
    if (!result?.ebpf_code) return

    try {
      await navigator.clipboard.writeText(result.ebpf_code)
      window.alert('eBPF C code copied!')
    } catch {
      window.alert('Unable to copy code.')
    }
  }

  const downloadCode = () => {
    if (!result?.ebpf_code) return

    const blob = new Blob([result.ebpf_code], {
      type: 'text/plain;charset=utf-8',
    })

    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')

    link.href = url
    link.download = 'policy.bpf.c'

    document.body.appendChild(link)
    link.click()
    link.remove()

    URL.revokeObjectURL(url)
  }

  const loadExample = (example) => {
    setSource(example.policy)
    setResult(null)
    setError('')
  }

  const renderConditions = () => {
    if (!result?.explanation || result.explanation.length === 0) {
      return (
        <div className="empty-conditions">
          No structured conditions returned by the compiler.
        </div>
      )
    }

    return result.explanation.map((item, index) => {
      if (item.logical_operator) {
        return (
          <div
            className="logical-operator"
            key={`logical-${index}`}
          >
            {item.logical_operator}
          </div>
        )
      }

      return (
        <div
          className="condition-row"
          key={`condition-${index}`}
        >
          <span className="condition-field">
            {FIELD_LABELS[item.field] || item.field}
          </span>

          <strong className="condition-operator">
            {OPERATOR_LABELS[item.operator] || item.operator}
          </strong>

          <code className="condition-value">
            {String(item.value)}
          </code>
        </div>
      )
    })
  }

  return (
    <div className="app">
      {/* ------------------------------------------------------- */}
      {/* HEADER */}
      {/* ------------------------------------------------------- */}
      <header className="navbar">
        <div className="brand">
          <div className="brand-icon">λ</div>

          <div>
            <h2>PolicyLang</h2>
            <span>Policy Compiler</span>
          </div>
        </div>

        <div className="compiler-status">
          <span className="status-dot"></span>
          Compiler v0.1
        </div>
      </header>

      <main>
        {/* ----------------------------------------------------- */}
        {/* HERO */}
        {/* ----------------------------------------------------- */}
        <section className="hero-section">
          <div className="eyebrow">
            eBPF POLICY COMPILER
          </div>

          <h1>
            Write policies.
            <br />
            <span>Generate eBPF.</span>
          </h1>

          <p>
            Define network security policies using PolicyLang and
            compile them into efficient eBPF programs.
          </p>

          <div className="stage-card">
            <strong>6</strong>

            <div>
              <b>Compilation stages</b>
              <span>Lexer → eBPF</span>
            </div>
          </div>
        </section>

        {/* ----------------------------------------------------- */}
        {/* POLICY EDITOR */}
        {/* ----------------------------------------------------- */}
        <section className="card editor-card">
          <div className="card-header">
            <div>
              <small>POLICY EDITOR</small>
              <h3>Policy Source</h3>
            </div>

            <span>policy.pl</span>
          </div>

          <textarea
            value={source}
            onChange={(event) => {
              setSource(event.target.value)

              if (result) {
                setResult(null)
              }

              if (error) {
                setError('')
              }
            }}
            spellCheck="false"
            placeholder="Write your PolicyLang policy here..."
          />

          {/* EXAMPLES */}
          <div className="examples">
            <span>EXAMPLES</span>

            {EXAMPLES.map((example) => (
              <button
                key={example.name}
                type="button"
                onClick={() => loadExample(example)}
              >
                {example.name}
              </button>
            ))}
          </div>

          {/* EDITOR FOOTER */}
          <div className="editor-footer">
            <span>PolicyLang syntax</span>

            <button
              type="button"
              className="compile-button"
              onClick={compilePolicy}
              disabled={loading || !source.trim()}
            >
              {loading ? 'Compiling...' : '▶ Compile Policy'}
            </button>
          </div>
        </section>

        {/* ----------------------------------------------------- */}
        {/* ERROR */}
        {/* ----------------------------------------------------- */}
        {error && (
          <section className="error-box">
            <strong>Compilation Failed</strong>
            <p>{error}</p>
          </section>
        )}

        {/* ----------------------------------------------------- */}
        {/* RESULTS */}
        {/* ----------------------------------------------------- */}
        {result && (
          <>
            {/* ------------------------------------------------- */}
            {/* EXPLAINABILITY */}
            {/* ------------------------------------------------- */}
            <section className="card explanation-card">
              <div className="card-header">
                <div>
                  <small>EXPLAINABILITY</small>
                  <h3>Policy Explanation</h3>
                </div>

                <span className="success-badge">
                  SUCCESS
                </span>
              </div>

              <div className="explanation-grid">
                {/* ACTION */}
                <div className="explanation-item">
                  <span>Action</span>

                  <strong>
                    {result.policy?.action || '—'}
                  </strong>
                </div>

                {/* DIRECTION */}
                <div className="explanation-item">
                  <span>Direction</span>

                  <strong>
                    {result.policy?.direction || '—'}
                  </strong>
                </div>

                {/* CONDITIONS */}
                <div className="explanation-item explanation-wide">
                  <span>Conditions</span>

                  <div className="conditions">
                    {renderConditions()}
                  </div>
                </div>

                {/* POLICY SUMMARY */}
                <div className="policy-summary">
                  <span>Policy Summary</span>

                  <p>
                    This policy will{' '}

                    <strong>
                      {result.policy?.action === 'ALLOW'
                        ? 'allow'
                        : 'deny'}
                    </strong>{' '}

                    matching{' '}

                    <strong>
                      {result.policy?.direction
                        ? result.policy.direction.toLowerCase()
                        : 'network'}
                    </strong>{' '}

                    traffic according to the conditions above.
                  </p>
                </div>

                {/* IR */}
                <div className="explanation-item explanation-wide">
                  <span>Intermediate Representation</span>

                  <code>
                    {result.ir ||
                      'IR not returned by the API'}
                  </code>
                </div>
              </div>
            </section>

            {/* ------------------------------------------------- */}
            {/* PIPELINE */}
            {/* ------------------------------------------------- */}
            <section className="card pipeline-card">
              <div className="card-header">
                <div>
                  <small>COMPILER PIPELINE</small>
                  <h3>Compilation Status</h3>
                </div>

                <span className="success-badge">
                  SUCCESS
                </span>
              </div>

              <div className="pipeline">
                {STAGES.map(([key, label]) => (
                  <div
                    className="pipeline-stage"
                    key={key}
                  >
                    <div className="stage-check">
                      ✓
                    </div>

                    <div>
                      <b>{label}</b>

                      <span>
                        {result.stages?.[key] === 'success'
                          ? 'Completed successfully'
                          : 'Not completed'}
                      </span>
                    </div>
                  </div>
                ))}
              </div>
            </section>

            {/* ------------------------------------------------- */}
            {/* GENERATED eBPF */}
            {/* ------------------------------------------------- */}
            <section className="card output-card">
              <div className="card-header">
                <div>
                  <small>COMPILER OUTPUT</small>
                  <h3>Generated eBPF C</h3>
                </div>

                <div className="output-actions">
                  <button
                    type="button"
                    onClick={copyCode}
                  >
                    Copy
                  </button>

                  <button
                    type="button"
                    onClick={downloadCode}
                  >
                    Download .bpf.c
                  </button>
                </div>
              </div>

              <div className="file-path">
                <span></span>
                <span></span>
                <span></span>

                {result.output_file ||
                  'build / policy.bpf.c'}
              </div>

              <pre>
                <code>
                  {result.ebpf_code}
                </code>
              </pre>
            </section>
          </>
        )}

        {/* ----------------------------------------------------- */}
        {/* INFORMATION CARDS */}
        {/* ----------------------------------------------------- */}
        <section className="info-grid">
          <div className="card info-card">
            <small>LANGUAGE</small>

            <h3>PolicyLang</h3>

            <p>
              Simple declarative network policy syntax.
            </p>
          </div>

          <div className="card info-card">
            <small>BACKEND</small>

            <h3>eBPF / TC</h3>

            <p>
              Generates Linux traffic-control programs.
            </p>
          </div>

          <div className="card info-card">
            <small>SUPPORTED</small>

            <h3>IPv4 · TCP · UDP · ICMP</h3>

            <p>
              Network fields, comparisons and logical
              conditions.
            </p>
          </div>
        </section>
      </main>

      {/* ------------------------------------------------------- */}
      {/* FOOTER */}
      {/* ------------------------------------------------------- */}
      <footer>
        <span>PolicyLang Compiler</span>
        <span>Built for programmable networking</span>
      </footer>
    </div>
  )
}

export default App