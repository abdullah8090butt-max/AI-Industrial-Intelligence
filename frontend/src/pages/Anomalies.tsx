import { useEffect, useState } from 'react';

import {
  DEFAULT_MACHINE,
  MACHINE_PROFILES,
  getMachineAnomaly,
  type AnomalyResponse,
} from '../services/api';

const MACHINES = [
  {
    id: 'M-001',
    name: 'Production Machine 01',
  },
  {
    id: 'M-002',
    name: 'Production Machine 02',
  },
  {
    id: 'M-003',
    name: 'Production Machine 03',
  },
];

function Anomalies() {
  const [selectedMachine, setSelectedMachine] = useState('M-001');
  const [anomaly, setAnomaly] = useState<AnomalyResponse | null>(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);

  const machine = MACHINES.find(
    (item) => item.id === selectedMachine
  );

  useEffect(() => {
    let mounted = true;

    const loadAnomalyData = async () => {
      try {
        if (mounted) {
          setLoading(true);
          setError(null);
        }

        const machineProfile =
          MACHINE_PROFILES[selectedMachine] ?? DEFAULT_MACHINE;

        const response = await getMachineAnomaly(machineProfile);

        if (!mounted) return;

        setAnomaly(response);
      } catch (err) {
        if (!mounted) return;

        setError(
          err instanceof Error
            ? err.message
            : 'Unable to load anomaly data.'
        );

        setAnomaly(null);
      } finally {
        if (mounted) {
          setLoading(false);
        }
      }
    };

    loadAnomalyData();

    return () => {
      mounted = false;
    };
  }, [selectedMachine]);

  const isAnomaly = anomaly?.anomaly_detected ?? false;

  const behaviorText = loading
    ? 'Analyzing...'
    : isAnomaly
      ? 'Abnormal Behavior'
      : 'Normal Behavior';

  const detectionText = loading
    ? 'Analyzing'
    : isAnomaly
      ? 'Anomaly Detected'
      : 'Normal';

  return (
    <div>
      <div className="page-header">
        <div>
          <h1>Anomaly Detection</h1>
          <p>
            AI-based detection and analysis of unusual machine behavior.
          </p>
        </div>

        <div className="status-badge">
          System Online
        </div>
      </div>

      <section className="dashboard-section">
        <div className="section-header">
          <div>
            <h2>Machine Selection</h2>
            <p>
              Select a machine to inspect its anomaly condition.
            </p>
          </div>
        </div>

        <div className="machine-selector">
          {MACHINES.map((item) => (
            <button
              key={item.id}
              type="button"
              className={
                selectedMachine === item.id
                  ? 'machine-button active'
                  : 'machine-button'
              }
              onClick={() => setSelectedMachine(item.id)}
            >
              <strong>{item.id}</strong>
              <span>{item.name}</span>
            </button>
          ))}
        </div>
      </section>

      <section className="dashboard-section">
        <div className="section-header">
          <div>
            <h2>Anomaly Analysis</h2>
            <p>
              AI analysis for {machine?.id} — {machine?.name}.
            </p>
          </div>
        </div>

        {error && (
          <div className="error-message">
            {error}
          </div>
        )}

        <div className="analysis-card">
          <div className="analysis-status">
            <span className="status-label">
              Detection Status
            </span>

            <span className="status-value">
              {detectionText}
            </span>
          </div>

          <div className="analysis-grid">
            <div className="analysis-item">
              <span>Machine</span>
              <strong>{selectedMachine}</strong>
            </div>

            <div className="analysis-item">
              <span>Behavior</span>
              <strong>{behaviorText}</strong>
            </div>

            <div className="analysis-item">
              <span>Anomaly Score</span>
              <strong>
                {anomaly
                  ? anomaly.anomaly_score.toFixed(4)
                  : '--'}
              </strong>
            </div>

            <div className="analysis-item">
              <span>AI Status</span>
              <strong>
                {loading ? 'Processing' : 'Connected'}
              </strong>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}

export default Anomalies;