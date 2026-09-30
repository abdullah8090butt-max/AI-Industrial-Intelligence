import type { ReactNode } from 'react';
import Sidebar from './Sidebar';

interface MainLayoutProps {
  children: ReactNode;
}

function MainLayout({ children }: MainLayoutProps) {
  return (
    <div className="app">
      <Sidebar />

      <div className="main-content">
        <div className="page-container">
          {children}
        </div>
      </div>
    </div>
  );
}

export default MainLayout;