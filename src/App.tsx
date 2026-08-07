import { useState } from 'react'
import {
  Activity,
  ArrowUpRight,
  Check,
  ChevronRight,
  Cloud,
  Cpu,
  Database,
  ExternalLink,
  FileCode2,
  KeyRound,
  Layers3,
  LockKeyhole,
  Menu,
  MoreHorizontal,
  Network,
  Plus,
  Search,
  Settings2,
  ShieldCheck,
  Sparkles,
  TerminalSquare,
  X,
  Zap,
} from 'lucide-react'

type Model = { name: string; size: string; role: string; status: 'ready' | 'cloud' | 'idle'; accent: string }

const models: Model[] = [
  { name: 'Qwen 3.5 · 9B', size: '6.6 GB', role: 'Primary coding', status: 'ready', accent: 'mint' },
  { name: 'Gemma 4 · 12B', size: '7.6 GB', role: 'Deep reasoning', status: 'idle', accent: 'gold' },
  { name: 'Qwen Coder · 1.5B', size: '986 MB', role: 'Autocomplete + routing', status: 'ready', accent: 'blue' },
]

const providers = [
  { name: 'Ollama', detail: 'Local runtime · 127.0.0.1:11434', state: 'Connected', icon: Cpu, color: 'mint' },
  { name: 'OpenRouter', detail: 'Cloud fallback · encrypted relay', state: 'Add API key', icon: Cloud, color: 'violet' },
  { name: 'Cloudflare Workers AI', detail: 'Agent endpoint · eu-west', state: 'Configure', icon: Network, color: 'orange' },
]

function WorkspaceView({
  view,
  onAddConnection,
  onSelectModel,
}: {
  view: string
  onAddConnection: () => void
  onSelectModel: (name: string) => void
}) {
  if (view === 'Models') return <>
    <section className="page-heading"><div><p className="eyebrow">Runtime inventory</p><h1>Model library</h1><p className="hero-copy">Choose the smallest capable model first. Active models stay on the internal SSD; the rest can live on your external drive.</p></div><button className="primary-button"><Plus size={17} /> Add model</button></section>
    <section className="model-detail-grid">{models.map((model) => <article className="model-detail-card" key={model.name}><div className={`model-orb ${model.accent}`}><Layers3 size={18} /></div><p className="eyebrow">{model.role}</p><h2>{model.name}</h2><div className="detail-line"><span>Footprint</span><strong>{model.size}</strong></div><div className="detail-line"><span>Availability</span><span className={`pill ${model.status}`}>{model.status === 'ready' ? <Check size={13} /> : <span className="tiny-dot" />}{model.status === 'ready' ? 'Ready locally' : 'Available'}</span></div><button className="outline-button" onClick={() => onSelectModel(model.name)}>{model.status === 'ready' ? 'Set as primary' : 'Load model'} <ChevronRight size={15} /></button></article>)}</section>
    <section className="section-block feature-panel"><div className="section-title"><div><p className="eyebrow">Recommended setup</p><h2>Balanced local fleet</h2></div><span className="auto-badge"><ShieldCheck size={13} /> 24 GB safe</span></div><div className="feature-grid"><span><strong>Primary</strong><small>Qwen 3.5 · 9B</small></span><span><strong>Fast path</strong><small>Qwen Coder · 1.5B</small></span><span><strong>Memory ceiling</strong><small>18 GB resident</small></span></div></section>
  </>

  if (view === 'Connections') return <>
    <section className="page-heading"><div><p className="eyebrow">Control plane</p><h1>Connections</h1><p className="hero-copy">Bring your own API keys and agent endpoints. Local requests stay on this Mac.</p></div><button className="primary-button" onClick={onAddConnection}><Plus size={17} /> Add connection</button></section>
    <section className="connection-page-list">{providers.map(({ name, detail, state, icon: Icon, color }) => <div className="provider-card" key={name}><span className={`connection-icon ${color}`}><Icon size={20} /></span><div className="connection-copy"><strong>{name}</strong><small>{detail}</small><span className={`connection-state ${state === 'Connected' ? 'connected' : ''}`}>{state === 'Connected' && <span className="status-dot" />}{state}</span></div><button className="outline-button" onClick={onAddConnection}>{state === 'Connected' ? 'Manage' : 'Configure'} <ChevronRight size={15} /></button></div>)}</section>
    <section className="agent-banner"><div className="agent-mark"><Network size={21} /></div><div className="agent-copy"><p className="eyebrow">Cloudflare Workers AI</p><h2>Agent-ready cloud escalation</h2><p>Connect a Worker endpoint with a scoped token. Cloud use remains opt-in and auditable.</p></div><button className="secondary-button" onClick={onAddConnection}>Configure agent <ExternalLink size={15} /></button></section>
  </>

  if (view === 'Repository') return <>
    <section className="page-heading"><div><p className="eyebrow">Local context</p><h1>Repository</h1><p className="hero-copy">Your codebase is indexed locally for focused, token-efficient context.</p></div><button className="primary-button"><Activity size={17} /> Rescan repository</button></section>
    <section className="status-grid"><div className="status-card"><div className="card-heading"><span className="icon-badge gold-bg"><FileCode2 size={18} /></span><span>Workspace</span></div><div className="metric"><strong>1,284</strong><span>files indexed</span></div><div className="repo-path"><span className="status-dot" /> sapna-rokai <ArrowUpRight size={14} /></div></div><div className="status-card"><div className="card-heading"><span className="icon-badge mint-bg"><Database size={18} /></span><span>Symbols</span></div><div className="metric"><strong>8,492</strong><span>definitions</span></div><div className="card-foot"><span>Functions, classes, imports</span><strong className="good">Ready</strong></div></div><div className="status-card"><div className="card-heading"><span className="icon-badge blue-bg"><Activity size={18} /></span><span>Git state</span></div><div className="metric"><strong>Clean</strong></div><div className="card-foot"><span>main · synced 2m ago</span><strong className="good">Ready</strong></div></div></section>
    <section className="section-block feature-panel"><div className="section-title"><div><p className="eyebrow">Context broker</p><h2>Retrieval priorities</h2></div><span className="auto-badge"><LockKeyhole size={13} /> Local only</span></div><div className="feature-grid"><span><strong>1. Open files</strong><small>Highest priority</small></span><span><strong>2. Git diff</strong><small>Changed code first</small></span><span><strong>3. Symbols</strong><small>Expand on demand</small></span></div></section>
  </>

  if (view === 'Usage & limits') return <>
    <section className="page-heading"><div><p className="eyebrow">Plan telemetry</p><h1>Usage & limits</h1><p className="hero-copy">Local inference is unlimited. Cloud providers use their own quotas and billing.</p></div><span className="auto-badge"><ShieldCheck size={13} /> Local plan</span></section>
    <section className="usage-panel"><div className="usage-summary"><span className="icon-badge mint-bg"><Cpu size={18} /></span><div><strong>Unlimited local inference</strong><small>Requests processed on this Mac</small></div><span className="usage-value">100%</span></div><div className="meter large"><span style={{ width: '100%' }} /></div><div className="usage-stats"><span><strong>2,841</strong><small>local requests this month</small></span><span><strong>0</strong><small>cloud requests</small></span><span><strong>0 GB</strong><small>code uploaded</small></span></div></section>
    <section className="section-block feature-panel"><div className="section-title"><div><p className="eyebrow">Cloud policy</p><h2>Fallback guardrails</h2></div><button className="outline-button" onClick={onAddConnection}>Manage providers <ChevronRight size={15} /></button></div><div className="feature-grid"><span><strong>Opt-in only</strong><small>Cloud fallback stays off</small></span><span><strong>Redaction</strong><small>Secrets filtered before send</small></span><span><strong>Audit trail</strong><small>Every request is visible</small></span></div></section>
  </>

  return <>
    <section className="page-heading"><div><p className="eyebrow">Application controls</p><h1>Settings</h1><p className="hero-copy">Tune privacy, memory, routing, and local service behavior.</p></div><button className="primary-button"><Check size={17} /> Saved</button></section>
    <section className="settings-list"><div className="setting-row"><div><strong>Private by default</strong><small>Never send repository code without approval.</small></div><span className="auto-badge"><LockKeyhole size={13} /> On</span></div><div className="setting-row"><div><strong>Memory safety guard</strong><small>Keep 2 GB free for macOS and the desktop app.</small></div><span className="auto-badge"><ShieldCheck size={13} /> Active</span></div><div className="setting-row"><div><strong>Local service</strong><small>Bound to 127.0.0.1 · authenticated IPC.</small></div><span className="connection-state connected"><span className="status-dot" /> Running</span></div></section>
  </>
}

function App() {
  const [activeNav, setActiveNav] = useState('Overview')
  const [showProvider, setShowProvider] = useState(false)
  const [cloudflareEnabled, setCloudflareEnabled] = useState(false)
  const [routing, setRouting] = useState('Balanced')

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand-lockup">
          <div className="brand-mark"><Sparkles size={16} /></div>
          <div><strong>flex</strong><span>fieldfare</span></div>
        </div>
        <div className="workspace-pill"><span className="status-dot" /> Local workspace <ChevronRight size={14} /></div>
        <nav>
          <p className="nav-label">Workspace</p>
          {['Overview', 'Models', 'Connections', 'Repository'].map((item) => (
            <button key={item} className={`nav-item ${activeNav === item ? 'active' : ''}`} onClick={() => setActiveNav(item)}>
              {item === 'Overview' && <Activity size={17} />}
              {item === 'Models' && <Layers3 size={17} />}
              {item === 'Connections' && <Network size={17} />}
              {item === 'Repository' && <FileCode2 size={17} />}
              <span>{item}</span>{activeNav === item && <span className="nav-active-bar" />}
            </button>
          ))}
          <p className="nav-label second">System</p>
          {['Usage & limits', 'Settings'].map((item) => (
            <button key={item} className={`nav-item ${activeNav === item ? 'active' : ''}`} onClick={() => setActiveNav(item)}>
              {item === 'Usage & limits' ? <Database size={17} /> : <Settings2 size={17} />}<span>{item}</span>
            </button>
          ))}
        </nav>
        <div className="sidebar-bottom">
          <div className="privacy-note"><LockKeyhole size={16} /><div><strong>Private by default</strong><span>Code stays on this Mac</span></div></div>
          <div className="user-row"><div className="avatar">RB</div><div><strong>Robin Bakshi</strong><span>Local plan</span></div><MoreHorizontal size={17} /></div>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar"><button className="mobile-menu" onClick={() => setActiveNav('Overview')} aria-label="Open overview"><Menu size={19} /></button><div className="crumb"><span>Workspace</span><ChevronRight size={14} /><strong>{activeNav}</strong></div><div className="top-actions"><span className="sync-status"><span className="status-dot" /> Everything synced</span><button className="icon-button" onClick={() => setActiveNav('Repository')} aria-label="Open repository"><Search size={18} /></button><button className="icon-button" onClick={() => setActiveNav('Settings')} aria-label="Open settings"><Settings2 size={18} /></button></div></header>

        <div className="content-wrap">
          {activeNav !== 'Overview' ? <WorkspaceView view={activeNav} onAddConnection={() => setShowProvider(true)} onSelectModel={() => setActiveNav('Models')} /> : <>
          <section className="hero-row"><div><p className="eyebrow">Friday, 07 August 2026 <span>·</span> M4 MacBook Pro</p><h1>Good afternoon, Robin.</h1><p className="hero-copy">Your local coding workspace is ready. One model is warm and your repository is indexed.</p></div><button className="primary-button" onClick={() => setShowProvider(true)}><Plus size={17} /> Add connection</button></section>

          <section className="status-grid">
            <div className="status-card memory-card"><div className="card-heading"><span className="icon-badge mint-bg"><Cpu size={18} /></span><span>Memory headroom</span><MoreHorizontal size={18} /></div><div className="metric"><strong>9.8</strong><span>GB free</span></div><div className="meter"><span style={{ width: '59%' }} /></div><div className="card-foot"><span>14.2 GB in use</span><strong className="good">Healthy</strong></div></div>
            <div className="status-card"><div className="card-heading"><span className="icon-badge blue-bg"><Zap size={18} /></span><span>Inference</span><MoreHorizontal size={18} /></div><div className="metric"><strong>18.4</strong><span>tok / sec</span></div><div className="mini-bars"><i /><i /><i /><i /><i /><i /><i /><i /><i /><i /><i /><i /></div><div className="card-foot"><span>Qwen 3.5 · 9B</span><strong className="good">Warm</strong></div></div>
            <div className="status-card"><div className="card-heading"><span className="icon-badge gold-bg"><FileCode2 size={18} /></span><span>Repository</span><MoreHorizontal size={18} /></div><div className="metric"><strong>1,284</strong><span>files indexed</span></div><div className="repo-path"><span className="status-dot" /> sapna-rokai <ArrowUpRight size={14} /></div><div className="card-foot"><span>Last scan 2m ago</span><strong>Ready</strong></div></div>
          </section>

          <section className="section-block"><div className="section-title"><div><p className="eyebrow">Runtime</p><h2>Local model fleet</h2></div><button className="text-button" onClick={() => setActiveNav('Models')}>Manage models <ArrowUpRight size={15} /></button></div><div className="model-table"><div className="table-head"><span>Model</span><span>Role</span><span>Footprint</span><span>Status</span><span /></div>{models.map((model) => <div className="model-row" key={model.name}><div className="model-name"><span className={`model-orb ${model.accent}`}><Layers3 size={16} /></span><strong>{model.name}</strong></div><span className="muted">{model.role}</span><span className="muted">{model.size}</span><span className={`pill ${model.status}`}>{model.status === 'ready' ? <Check size={13} /> : model.status === 'cloud' ? <Cloud size={13} /> : <span className="tiny-dot" />}{model.status === 'ready' ? 'Ready' : model.status === 'cloud' ? 'Cloud' : 'Available'}</span><button className="row-arrow"><ChevronRight size={17} /></button></div>)}</div></section>

          <div className="lower-grid"><section className="section-block connections"><div className="section-title"><div><p className="eyebrow">Control plane</p><h2>Connections</h2></div><button className="icon-button bordered" onClick={() => setShowProvider(true)}><Plus size={17} /></button></div><div className="connection-list">{providers.map(({ name, detail, state, icon: Icon, color }) => <button className="connection-row" key={name} onClick={() => setShowProvider(true)}><span className={`connection-icon ${color}`}><Icon size={18} /></span><span className="connection-copy"><strong>{name}</strong><small>{detail}</small></span><span className={`connection-state ${state === 'Connected' ? 'connected' : ''}`}>{state === 'Connected' && <span className="status-dot" />}{state}</span><ChevronRight size={16} /></button>)}</div></section><section className="section-block routing-card"><div className="section-title"><div><p className="eyebrow">Orchestration</p><h2>Routing policy</h2></div><span className="auto-badge"><Sparkles size={13} /> Auto</span></div><p className="routing-copy">Flex chooses the smallest capable model first, then escalates when the task needs more context or reasoning.</p><div className="segmented">{['Speed', 'Balanced', 'Quality'].map((item) => <button key={item} className={routing === item ? 'selected' : ''} onClick={() => setRouting(item)}>{item}</button>)}</div><div className="routing-rule"><div className="rule-icon"><ShieldCheck size={16} /></div><div><strong>Cloud fallback is off</strong><span>Local-only requests are protected</span></div><button className={`switch ${cloudflareEnabled ? 'on' : ''}`} onClick={() => setCloudflareEnabled(!cloudflareEnabled)} aria-label="Toggle cloud fallback"><span /></button></div></section></div>

          <section className="agent-banner"><div className="agent-mark"><Network size={21} /></div><div className="agent-copy"><p className="eyebrow">Cloudflare Workers AI</p><h2>Bring your own agent endpoint.</h2><p>Connect a Worker agent for approved cloud tasks without moving your local workflow.</p></div><button className="secondary-button" onClick={() => setShowProvider(true)}>Configure agent <ExternalLink size={15} /></button></section>
          </>}
        </div>
      </main>
      {showProvider && <div className="modal-backdrop" onClick={() => setShowProvider(false)}><div className="modal" onClick={(event) => event.stopPropagation()}><div className="modal-top"><div><p className="eyebrow">Connection setup</p><h2>Add an AI provider</h2></div><button className="icon-button" onClick={() => setShowProvider(false)}><X size={18} /></button></div><p className="modal-copy">Credentials stay in your macOS Keychain in the desktop app. This preview stores configuration locally.</p><label>Provider<select><option>Cloudflare Workers AI Agent</option><option>OpenRouter</option><option>OpenAI-compatible API</option><option>Custom local endpoint</option></select></label><label>Endpoint URL<input placeholder="https://your-agent.workers.dev" /></label><label>API token<input type="password" placeholder="Paste token" /></label><div className="modal-actions"><button className="text-button" onClick={() => setShowProvider(false)}>Cancel</button><button className="primary-button" onClick={() => setShowProvider(false)}><KeyRound size={16} /> Save connection</button></div></div></div>}
    </div>
  )
}

export default App
