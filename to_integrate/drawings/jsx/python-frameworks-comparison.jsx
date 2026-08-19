import React, { useState } from 'react';

const frameworks = [
  {
    name: 'Django',
    type: 'Full-Stack',
    released: 2005,
    githubStars: '82k+',
    async: 'Partial (ASGI)',
    performance: '~3,000 req/s',
    learningCurve: 'Steep',
    documentation: 'Excellent',
    bestFor: 'Large apps, CMS, admin-heavy',
    builtIn: 'ORM, Auth, Admin, Forms, Templates',
    typing: 'Optional',
    companies: 'Instagram, Pinterest, Mozilla',
    pros: ['Batteries included', 'Mature ecosystem', 'Strong security', 'Great admin panel'],
    cons: ['Monolithic', 'Overkill for small projects', 'Slower performance'],
  },
  {
    name: 'FastAPI',
    type: 'Micro/API',
    released: 2018,
    githubStars: '75k+',
    async: 'Native (async/await)',
    performance: '~20,000+ req/s',
    learningCurve: 'Moderate',
    documentation: 'Excellent',
    bestFor: 'APIs, microservices, ML inference',
    builtIn: 'Validation, Auto-docs, Dependency injection',
    typing: 'Required (type hints)',
    companies: 'Microsoft, Uber, Netflix',
    pros: ['Extremely fast', 'Auto OpenAPI docs', 'Type safety', 'Modern Python'],
    cons: ['Newer ecosystem', 'No built-in ORM', 'Requires async knowledge'],
  },
  {
    name: 'Flask',
    type: 'Micro',
    released: 2010,
    githubStars: '68k+',
    async: 'Limited (via extensions)',
    performance: '~4,000-5,000 req/s',
    learningCurve: 'Easy',
    documentation: 'Good',
    bestFor: 'Small apps, prototypes, learning',
    builtIn: 'Routing, Templates (Jinja2), Sessions',
    typing: 'Optional',
    companies: 'Netflix, Reddit, Airbnb',
    pros: ['Simple & flexible', 'Large extension ecosystem', 'Easy to learn', 'Unopinionated'],
    cons: ['Manual assembly needed', 'Sync by default', 'Less structured'],
  },
  {
    name: 'Tornado',
    type: 'Async',
    released: 2009,
    githubStars: '21k+',
    async: 'Native (event loop)',
    performance: '~8,000-12,000 req/s',
    learningCurve: 'Moderate',
    documentation: 'Good',
    bestFor: 'WebSockets, long-polling, real-time',
    builtIn: 'Async HTTP client, WebSocket support',
    typing: 'Optional',
    companies: 'Facebook, Quora',
    pros: ['Excellent for real-time', 'Built-in async', 'WebSocket native'],
    cons: ['Smaller ecosystem', 'Less conventional', 'Dated API design'],
  },
  {
    name: 'Sanic',
    type: 'Async',
    released: 2016,
    githubStars: '18k+',
    async: 'Native (async/await)',
    performance: '~15,000+ req/s',
    learningCurve: 'Moderate',
    documentation: 'Good',
    bestFor: 'High-performance APIs',
    builtIn: 'Routing, Middleware, WebSockets',
    typing: 'Optional',
    companies: 'Various startups',
    pros: ['Very fast', 'Flask-like syntax', 'Built for speed'],
    cons: ['Smaller community', 'Less mature', 'Fewer extensions'],
  },
  {
    name: 'Pyramid',
    type: 'Full-Stack',
    released: 2010,
    githubStars: '4k+',
    async: 'Limited',
    performance: '~3,000-5,000 req/s',
    learningCurve: 'Moderate',
    documentation: 'Excellent',
    bestFor: 'Flexible large projects',
    builtIn: 'URL dispatch, Auth, Templating',
    typing: 'Optional',
    companies: 'Mozilla, Yelp, Dropbox',
    pros: ['Highly flexible', 'Scales well', 'URL dispatch + traversal'],
    cons: ['Smaller community', 'Less opinionated', 'Steeper than Flask'],
  },
  {
    name: 'Bottle',
    type: 'Micro',
    released: 2009,
    githubStars: '8k+',
    async: 'No',
    performance: '~3,000 req/s',
    learningCurve: 'Very Easy',
    documentation: 'Good',
    bestFor: 'Tiny apps, single-file apps, APIs',
    builtIn: 'Routing, Templates, Server',
    typing: 'Optional',
    companies: 'Small projects',
    pros: ['Single file, no deps', 'Ultra lightweight', 'Embeddable'],
    cons: ['Very limited', 'No async', 'Not for large apps'],
  },
  {
    name: 'CherryPy',
    type: 'Full-Stack',
    released: 2002,
    githubStars: '2k+',
    async: 'Limited',
    performance: '~2,000-3,000 req/s',
    learningCurve: 'Easy',
    documentation: 'Fair',
    bestFor: 'Standalone apps, OOP style',
    builtIn: 'HTTP server, Sessions, Caching',
    typing: 'Optional',
    companies: 'Various enterprises',
    pros: ['Object-oriented', 'Built-in server', 'Stable'],
    cons: ['Dated', 'Small community', 'Limited modern features'],
  },
  {
    name: 'Dash',
    type: 'Specialized',
    released: 2017,
    githubStars: '21k+',
    async: 'Limited',
    performance: 'N/A (UI focused)',
    learningCurve: 'Easy-Moderate',
    documentation: 'Excellent',
    bestFor: 'Data dashboards, visualizations',
    builtIn: 'Plotly charts, React components',
    typing: 'Optional',
    companies: 'Data teams everywhere',
    pros: ['No JS needed', 'Beautiful charts', 'Reactive UI'],
    cons: ['Not general purpose', 'Limited customization', 'Plotly lock-in'],
  },
  {
    name: 'Reflex',
    type: 'Full-Stack',
    released: 2022,
    githubStars: '20k+',
    async: 'Yes',
    performance: 'Moderate',
    learningCurve: 'Easy',
    documentation: 'Good',
    bestFor: 'Full-stack Python (no JS)',
    builtIn: '60+ UI components, Auth, DB',
    typing: 'Required',
    companies: 'Growing adoption',
    pros: ['Pure Python full-stack', 'React under hood', 'One-command deploy'],
    cons: ['Very new', 'Smaller ecosystem', 'Less flexibility'],
  },
  {
    name: 'Quart',
    type: 'Async',
    released: 2017,
    githubStars: '3k+',
    async: 'Native (async/await)',
    performance: '~9,000 req/s',
    learningCurve: 'Easy (Flask users)',
    documentation: 'Good',
    bestFor: 'Async Flask migration',
    builtIn: 'Flask-compatible API',
    typing: 'Optional',
    companies: 'Various',
    pros: ['Flask-compatible', 'Native async', 'Easy migration'],
    cons: ['Smaller ecosystem', 'Less mature', 'Flask extension compatibility varies'],
  },
  {
    name: 'Falcon',
    type: 'Micro/API',
    released: 2013,
    githubStars: '9k+',
    async: 'Yes (v3+)',
    performance: '~10,000+ req/s',
    learningCurve: 'Moderate',
    documentation: 'Good',
    bestFor: 'High-performance REST APIs',
    builtIn: 'Routing, Middleware, WSGI/ASGI',
    typing: 'Optional',
    companies: 'LinkedIn, OpenStack',
    pros: ['Very fast', 'Minimal overhead', 'REST-focused'],
    cons: ['API-only', 'No templating', 'Bare-bones'],
  },
];

const typeColors = {
  'Full-Stack': { bg: '#1e3a5f', text: '#7dd3fc' },
  'Micro': { bg: '#3d1f1f', text: '#fca5a5' },
  'Micro/API': { bg: '#3d2d1f', text: '#fcd34d' },
  'Async': { bg: '#1f3d2d', text: '#86efac' },
  'Specialized': { bg: '#3d1f3d', text: '#d8b4fe' },
};

const perfColors = (perf) => {
  if (perf.includes('20,000') || perf.includes('15,000')) return '#22c55e';
  if (perf.includes('10,000') || perf.includes('9,000') || perf.includes('8,000')) return '#84cc16';
  if (perf.includes('5,000') || perf.includes('4,000')) return '#eab308';
  return '#f97316';
};

export default function PythonFrameworksComparison() {
  const [sortBy, setSortBy] = useState('githubStars');
  const [filterType, setFilterType] = useState('All');
  const [expandedRow, setExpandedRow] = useState(null);
  const [searchTerm, setSearchTerm] = useState('');

  const filteredFrameworks = frameworks
    .filter(f => filterType === 'All' || f.type === filterType || (filterType === 'Async-Capable' && (f.async.includes('Native') || f.async === 'Yes')))
    .filter(f => f.name.toLowerCase().includes(searchTerm.toLowerCase()) || f.bestFor.toLowerCase().includes(searchTerm.toLowerCase()))
    .sort((a, b) => {
      if (sortBy === 'githubStars') {
        const aNum = parseInt(a.githubStars.replace(/[^0-9]/g, ''));
        const bNum = parseInt(b.githubStars.replace(/[^0-9]/g, ''));
        return bNum - aNum;
      }
      if (sortBy === 'released') return b.released - a.released;
      if (sortBy === 'name') return a.name.localeCompare(b.name);
      if (sortBy === 'performance') {
        const getPerf = (p) => {
          const match = p.match(/[\d,]+/);
          return match ? parseInt(match[0].replace(',', '')) : 0;
        };
        return getPerf(b.performance) - getPerf(a.performance);
      }
      return 0;
    });

  const types = ['All', 'Full-Stack', 'Micro', 'Micro/API', 'Async', 'Specialized', 'Async-Capable'];

  return (
    <div style={{
      minHeight: '100vh',
      background: 'linear-gradient(135deg, #0f0f0f 0%, #1a1a2e 50%, #0f0f0f 100%)',
      color: '#e5e5e5',
      fontFamily: '"IBM Plex Sans", -apple-system, sans-serif',
      padding: '32px 24px',
    }}>
      <style>{`
        @import url('https://fonts.googleapis.com/css2?family=IBM+Plex+Sans:wght@400;500;600&family=JetBrains+Mono:wght@400;500&display=swap');
        * { box-sizing: border-box; }
        ::-webkit-scrollbar { width: 8px; height: 8px; }
        ::-webkit-scrollbar-track { background: #1a1a1a; }
        ::-webkit-scrollbar-thumb { background: #404040; border-radius: 4px; }
        ::-webkit-scrollbar-thumb:hover { background: #505050; }
      `}</style>
      
      <header style={{ maxWidth: '1400px', margin: '0 auto 32px', textAlign: 'center' }}>
        <h1 style={{
          fontSize: '2.5rem',
          fontWeight: 600,
          background: 'linear-gradient(135deg, #60a5fa 0%, #a78bfa 50%, #f472b6 100%)',
          WebkitBackgroundClip: 'text',
          WebkitTextFillColor: 'transparent',
          marginBottom: '8px',
          letterSpacing: '-0.02em',
        }}>
          Python Web Frameworks
        </h1>
        <p style={{ color: '#888', fontSize: '1.1rem', marginBottom: '24px' }}>
          Comprehensive comparison of {frameworks.length} frameworks • Updated 2025
        </p>
        
        <div style={{ display: 'flex', gap: '16px', justifyContent: 'center', flexWrap: 'wrap', marginBottom: '16px' }}>
          <input
            type="text"
            placeholder="Search frameworks..."
            value={searchTerm}
            onChange={(e) => setSearchTerm(e.target.value)}
            style={{
              padding: '10px 16px',
              borderRadius: '8px',
              border: '1px solid #333',
              background: '#1a1a1a',
              color: '#e5e5e5',
              fontSize: '0.95rem',
              width: '220px',
              outline: 'none',
            }}
          />
          
          <select
            value={sortBy}
            onChange={(e) => setSortBy(e.target.value)}
            style={{
              padding: '10px 16px',
              borderRadius: '8px',
              border: '1px solid #333',
              background: '#1a1a1a',
              color: '#e5e5e5',
              fontSize: '0.95rem',
              cursor: 'pointer',
            }}
          >
            <option value="githubStars">Sort: GitHub Stars</option>
            <option value="performance">Sort: Performance</option>
            <option value="released">Sort: Newest First</option>
            <option value="name">Sort: Alphabetical</option>
          </select>
        </div>
        
        <div style={{ display: 'flex', gap: '8px', justifyContent: 'center', flexWrap: 'wrap' }}>
          {types.map(type => (
            <button
              key={type}
              onClick={() => setFilterType(type)}
              style={{
                padding: '8px 16px',
                borderRadius: '20px',
                border: filterType === type ? '1px solid #60a5fa' : '1px solid #333',
                background: filterType === type ? 'rgba(96, 165, 250, 0.15)' : 'transparent',
                color: filterType === type ? '#60a5fa' : '#888',
                fontSize: '0.85rem',
                cursor: 'pointer',
                transition: 'all 0.2s ease',
              }}
            >
              {type}
            </button>
          ))}
        </div>
      </header>

      <div style={{ maxWidth: '1400px', margin: '0 auto', overflowX: 'auto' }}>
        <table style={{ width: '100%', borderCollapse: 'collapse', fontSize: '0.9rem' }}>
          <thead>
            <tr style={{ borderBottom: '2px solid #333' }}>
              {['Framework', 'Type', 'Released', 'Stars', 'Async', 'Performance', 'Learning', 'Best For'].map(header => (
                <th key={header} style={{
                  padding: '16px 12px',
                  textAlign: 'left',
                  color: '#888',
                  fontWeight: 500,
                  fontSize: '0.8rem',
                  textTransform: 'uppercase',
                  letterSpacing: '0.05em',
                }}>
                  {header}
                </th>
              ))}
            </tr>
          </thead>
          <tbody>
            {filteredFrameworks.map((fw, idx) => (
              <React.Fragment key={fw.name}>
                <tr
                  onClick={() => setExpandedRow(expandedRow === idx ? null : idx)}
                  style={{
                    borderBottom: '1px solid #252525',
                    cursor: 'pointer',
                    background: expandedRow === idx ? 'rgba(96, 165, 250, 0.05)' : 'transparent',
                    transition: 'background 0.2s ease',
                  }}
                  onMouseEnter={(e) => e.currentTarget.style.background = 'rgba(255,255,255,0.02)'}
                  onMouseLeave={(e) => e.currentTarget.style.background = expandedRow === idx ? 'rgba(96, 165, 250, 0.05)' : 'transparent'}
                >
                  <td style={{ padding: '16px 12px', fontWeight: 600, color: '#fff', fontFamily: '"JetBrains Mono", monospace' }}>
                    {fw.name}
                    <span style={{ marginLeft: '8px', color: '#555', fontSize: '0.75rem' }}>
                      {expandedRow === idx ? '▼' : '▶'}
                    </span>
                  </td>
                  <td style={{ padding: '16px 12px' }}>
                    <span style={{
                      padding: '4px 10px',
                      borderRadius: '4px',
                      fontSize: '0.75rem',
                      fontWeight: 500,
                      background: typeColors[fw.type]?.bg || '#333',
                      color: typeColors[fw.type]?.text || '#999',
                    }}>
                      {fw.type}
                    </span>
                  </td>
                  <td style={{ padding: '16px 12px', color: '#888', fontFamily: '"JetBrains Mono", monospace' }}>{fw.released}</td>
                  <td style={{ padding: '16px 12px', color: '#fbbf24', fontFamily: '"JetBrains Mono", monospace' }}>★ {fw.githubStars}</td>
                  <td style={{ padding: '16px 12px' }}>
                    <span style={{
                      color: fw.async.includes('Native') || fw.async === 'Yes' ? '#22c55e' : fw.async.includes('Partial') || fw.async.includes('Limited') ? '#eab308' : '#ef4444',
                    }}>
                      {fw.async.includes('Native') || fw.async === 'Yes' ? '✓' : fw.async === 'No' ? '✗' : '◐'} {fw.async.split(' ')[0]}
                    </span>
                  </td>
                  <td style={{ padding: '16px 12px', color: perfColors(fw.performance), fontFamily: '"JetBrains Mono", monospace', fontSize: '0.85rem' }}>
                    {fw.performance}
                  </td>
                  <td style={{ padding: '16px 12px', color: '#888' }}>{fw.learningCurve}</td>
                  <td style={{ padding: '16px 12px', color: '#a1a1aa', maxWidth: '200px' }}>{fw.bestFor}</td>
                </tr>
                {expandedRow === idx && (
                  <tr style={{ background: 'rgba(30, 30, 40, 0.5)' }}>
                    <td colSpan={8} style={{ padding: '20px 24px' }}>
                      <div style={{ display: 'grid', gridTemplateColumns: 'repeat(auto-fit, minmax(250px, 1fr))', gap: '24px' }}>
                        <div>
                          <h4 style={{ color: '#60a5fa', marginBottom: '8px', fontSize: '0.85rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Built-in Features</h4>
                          <p style={{ color: '#a1a1aa', lineHeight: 1.6 }}>{fw.builtIn}</p>
                        </div>
                        <div>
                          <h4 style={{ color: '#22c55e', marginBottom: '8px', fontSize: '0.85rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Pros</h4>
                          <ul style={{ margin: 0, paddingLeft: '16px', color: '#a1a1aa' }}>
                            {fw.pros.map(pro => <li key={pro} style={{ marginBottom: '4px' }}>{pro}</li>)}
                          </ul>
                        </div>
                        <div>
                          <h4 style={{ color: '#ef4444', marginBottom: '8px', fontSize: '0.85rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Cons</h4>
                          <ul style={{ margin: 0, paddingLeft: '16px', color: '#a1a1aa' }}>
                            {fw.cons.map(con => <li key={con} style={{ marginBottom: '4px' }}>{con}</li>)}
                          </ul>
                        </div>
                        <div>
                          <h4 style={{ color: '#a78bfa', marginBottom: '8px', fontSize: '0.85rem', textTransform: 'uppercase', letterSpacing: '0.05em' }}>Details</h4>
                          <p style={{ color: '#a1a1aa', marginBottom: '4px' }}><strong>Type hints:</strong> {fw.typing}</p>
                          <p style={{ color: '#a1a1aa', marginBottom: '4px' }}><strong>Docs:</strong> {fw.documentation}</p>
                          <p style={{ color: '#a1a1aa' }}><strong>Used by:</strong> {fw.companies}</p>
                        </div>
                      </div>
                    </td>
                  </tr>
                )}
              </React.Fragment>
            ))}
          </tbody>
        </table>
      </div>

      <footer style={{ maxWidth: '1400px', margin: '48px auto 0', padding: '24px', borderTop: '1px solid #252525', color: '#666', fontSize: '0.8rem', textAlign: 'center' }}>
        <p>Performance figures are approximate benchmarks under optimal conditions. Actual performance varies by workload, configuration, and hardware.</p>
        <p style={{ marginTop: '8px' }}>Click any row to expand details • Data compiled from official docs, GitHub, and community benchmarks</p>
      </footer>
    </div>
  );
}
