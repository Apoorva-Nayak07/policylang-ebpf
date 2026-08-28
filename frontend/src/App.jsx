import { useState } from 'react'
import './App.css'

const DEFAULT_POLICY = `allow ingress
when source.ip == "10.0.0.5"
and destination.port == 443`

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
      setError(err.message)
    } finally {
      setLoading(false)
    }
  }

  const copyCode = async () => {
    if (!result?.ebpf_code) return

    await navigator.clipboard.writeText(result.ebpf_code)
    alert('eBPF C code copied!')
  }

  const downloadCode = () => {
    if (!result?.ebpf_code) return

    const blob = new Blob([result.ebpf_code], {
      type: 'text/plain',
    })

    const url = URL.createObjectURL(blob)
    const link = document.createElement('a')

    link.href = url
    link.download = 'policy.bpf.c'
    link.click()

    URL.revokeObjectURL(url)
  }

  const stages = [
    ['lexer', 'Lexer'],
    ['parser', 'Parser'],
    ['semantic_analysis', 'Semantic Analysis'],
    ['ir_lowering', 'IR Lowering'],
    ['optimization', 'Optimizer'],
    ['ebpf_generation', 'eBPF Generation'],
  ]

  return (
    <div className="app">
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
        <section className="hero-section">
          <div className="eyebrow">eBPF POLICY COMPILER</div>

          <h1>
            Write policies.
            <br />
            <span>Generate eBPF.</span>
          </h1>

          <p>
            Define network security policies using PolicyLang and compile them
            into efficient eBPF programs.
          </p>

          <div className="stage-card">
            <strong>6</strong>

            <div>
              <b>Compilation stages</b>
              <span>Lexer → eBPF</span>
            </div>
          </div>
        </section>

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
            onChange={(event) => setSource(event.target.value)}
            spellCheck="false"
            placeholder="Write your PolicyLang policy here..."
          />

          <div className="editor-footer">
            <span>PolicyLang syntax</span>

            <button
              className="compile-button"
              onClick={compilePolicy}
              disabled={loading}
            >
              {loading ? 'Compiling...' : '▶ Compile Policy'}
            </button>
          </div>
        </section>

        {error && (
          <section className="error-box">
            <strong>Compilation Failed</strong>
            <p>{error}</p>
          </section>
        )}

        {result && (
          <>
            <section className="card pipeline-card">
              <div className="card-header">
                <div>
                  <small>COMPILER PIPELINE</small>
                  <h3>Compilation Status</h3>
                </div>

                <span className="success-badge">SUCCESS</span>
              </div>

              <div className="pipeline">
                {stages.map(([key, label]) => (
                  <div className="pipeline-stage" key={key}>
                    <div className="stage-check">✓</div>

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

            <section className="card output-card">
              <div className="card-header">
                <div>
                  <small>COMPILER OUTPUT</small>
                  <h3>Generated eBPF C</h3>
                </div>

                <div className="output-actions">
                  <button onClick={copyCode}>Copy</button>
                  <button onClick={downloadCode}>Download .bpf.c</button>
                </div>
              </div>

              <div className="file-path">
                <span></span>
                <span></span>
                <span></span>
                build / policy.bpf.c
              </div>

              <pre>
                <code>{result.ebpf_code}</code>
              </pre>
            </section>
          </>
        )}

        <section className="info-grid">
          <div className="card info-card">
            <small>LANGUAGE</small>
            <h3>PolicyLang</h3>
            <p>Simple declarative network policy syntax.</p>
          </div>

          <div className="card info-card">
            <small>BACKEND</small>
            <h3>eBPF / TC</h3>
            <p>Generates Linux traffic-control programs.</p>
          </div>

          <div className="card info-card">
            <small>SUPPORTED</small>
            <h3>IPv4 · TCP · UDP · ICMP</h3>
            <p>Network fields, comparisons and logical conditions.</p>
          </div>
        </section>
      </main>

      <footer>
        <span>PolicyLang Compiler</span>
        <span>Built for programmable networking</span>
      </footer>
    </div>
  )
}

export default App