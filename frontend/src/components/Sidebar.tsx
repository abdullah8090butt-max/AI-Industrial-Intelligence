interface NavigationItem {
  label: string;
  path: string;
  icon: string;
}

const navigationItems: NavigationItem[] = [
  {
    label: 'Dashboard',
    path: '/',
    icon: '▦',
  },
  {
    label: 'Machine Monitoring',
    path: '/machines',
    icon: '⚙',
  },
  {
    label: 'Anomalies',
    path: '/anomalies',
    icon: '⚠',
  },
  {
    label: 'Predictive Maintenance',
    path: '/maintenance',
    icon: '🔧',
  },
  {
    label: 'Forecasting',
    path: '/forecasting',
    icon: '↗',
  },
  {
    label: 'AI Explanation',
    path: '/explanation',
    icon: '✦',
  },
  {
    label: 'AI Copilot',
    path: '/copilot',
    icon: '◉',
  },
  {
    label: 'Reports',
    path: '/reports',
    icon: '▤',
  },
];

function Sidebar() {
  return (
    <aside className="sidebar">
      <div className="sidebar-brand">
        <div className="brand-icon">AI</div>

        <div>
          <h2>Industrial AI</h2>
          <span>Intelligence System</span>
        </div>
      </div>

      <nav className="sidebar-navigation">
        <p className="sidebar-section-title">MAIN MENU</p>

        {navigationItems.map((item) => (
          <a
            key={item.path}
            href={item.path}
            className={`sidebar-link ${
              item.path === '/' ? 'sidebar-link-active' : ''
            }`}
          >
            <span className="sidebar-icon">{item.icon}</span>

            <span>{item.label}</span>
          </a>
        ))}
      </nav>
    </aside>
  );
}

export default Sidebar;