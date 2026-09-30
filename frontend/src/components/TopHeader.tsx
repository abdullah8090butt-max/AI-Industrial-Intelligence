interface TopHeaderProps {
  title: string;
  subtitle?: string;
}

function TopHeader({ title, subtitle }: TopHeaderProps) {
  return (
    <header className="top-header">
      <div>
        <h1 className="top-header-title">{title}</h1>

        {subtitle && (
          <p className="top-header-subtitle">
            {subtitle}
          </p>
        )}
      </div>

      <div className="top-header-status">
        <span className="status-dot" />

        <div>
          <strong>System Online</strong>
          <span>Monitoring active</span>
        </div>
      </div>
    </header>
  );
}

export default TopHeader;