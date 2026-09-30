import { useEffect, useState } from 'react';

import {
  DEFAULT_MACHINE,
  MACHINE_PROFILES,
  getMachineFailureRisk,
  getMachineRecommendations,
  type FailureRiskResponse,
  type MaintenanceRecommendationResponse,
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

function PredictiveMaintenance() {
  const [selectedMachine, setSelectedMachine] =
    useState('M-001');

  const [failureRisk, setFailureRisk] =
    useState<FailureRiskResponse | null>(null);

  const [recommendations, setRecommendations] =
    useState<MaintenanceRecommendationResponse | null>(
      null
    );

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState<string | null>(
    null
  );

  const machine = MACHINES.find(
    (item) => item.id === selectedMachine
  );

  useEffect(() => {
    let mounted = true;

    const loadMaintenanceData = async () => {
      if (mounted) {
        setLoading(true);
        setError(null);

        // Clear previous machine results immediately.
        setFailureRisk(null);
        setRecommendations(null);
      }

      try {
        const machineProfile =
          MACHINE_PROFILES[selectedMachine] ??
          DEFAULT_MACHINE;

        const [
          failureRiskResponse,
          recommendationResponse,
        ] = await Promise.all([
          getMachineFailureRisk(machineProfile),
          getMachineRecommendations(machineProfile),
        ]);

        if (!mounted) return;

        setFailureRisk(failureRiskResponse);
        setRecommendations(recommendationResponse);
      } catch (err) {
        if (!mounted) return;

        setFailureRisk(null);
        setRecommendations(null);

        setError(
          err instanceof Error
            ? err.message
            : 'Unable to load predictive maintenance data.'
        );
      } finally {
        if (mounted) {
          setLoading(false);
        }
      }
    };

    loadMaintenanceData();

    return () => {
      mounted = false;
    };
  }, [selectedMachine]);

  const riskLevel =
    recommendations?.risk_level ?? '--';

  const priority =
    recommendations?.maintenance?.priority ?? '--';

  const predictedFailure =
    failureRisk?.predicted_failure ?? false;

  const failureRiskValue =
    failureRisk?.failure_risk ?? null;

  const statusText = loading
    ? 'Analyzing...'
    : predictedFailure
      ? 'Maintenance Required'
      : 'No Immediate Failure Predicted';

  const riskBadgeStyle = {
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '8px 14px',
    borderRadius: '999px',
    fontSize: '13px',
    fontWeight: 700,
    background:
      riskLevel === 'Critical'
        ? '#fee2e2'
        : riskLevel === 'Warning'
          ? '#fef3c7'
          : '#dcfce7',
    color:
      riskLevel === 'Critical'
        ? '#b91c1c'
        : riskLevel === 'Warning'
          ? '#92400e'
          : '#166534',
  };

  const priorityBadgeStyle = {
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '8px 14px',
    borderRadius: '999px',
    fontSize: '13px',
    fontWeight: 700,
    background:
      priority === 'High'
        ? '#fee2e2'
        : priority === 'Medium'
          ? '#fef3c7'
          : '#dcfce7',
    color:
      priority === 'High'
        ? '#b91c1c'
        : priority === 'Medium'
          ? '#92400e'
          : '#166534',
  };

  const failureBadgeStyle = {
    display: 'inline-flex',
    alignItems: 'center',
    justifyContent: 'center',
    padding: '8px 14px',
    borderRadius: '999px',
    fontSize: '13px',
    fontWeight: 700,
    background: predictedFailure
      ? '#fee2e2'
      : '#dcfce7',
    color: predictedFailure
      ? '#b91c1c'
      : '#166534',
  };

  return (
    <div>
      <div className="page-header">
        <div>
          <h1>Predictive Maintenance</h1>

          <p>
            AI-powered failure risk assessment and
            maintenance intelligence.
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
              Select a machine to view its predictive
              maintenance condition.
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
              onClick={() =>
                setSelectedMachine(item.id)
              }
              disabled={loading}
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
            <h2>Maintenance Intelligence</h2>

            <p>
              AI predictive maintenance analysis for{' '}
              {machine?.id} — {machine?.name}.
            </p>
          </div>
        </div>

        {error && (
          <div className="error-message">
            <strong>Backend Error</strong>
            <p>{error}</p>
          </div>
        )}

        <div className="maintenance-card">
          <div className="maintenance-status">
            <span className="status-label">
              Maintenance Status
            </span>

            <span className="status-value">
              {statusText}
            </span>
          </div>

          <div className="analysis-grid">
            <div className="analysis-item">
              <span>Machine</span>

              <strong>{selectedMachine}</strong>
            </div>

            <div className="analysis-item">
              <span>Failure Risk</span>

              <strong>
                {loading
                  ? 'Analyzing...'
                  : failureRiskValue !== null
                    ? `${failureRiskValue}%`
                    : '--'}
              </strong>
            </div>

            <div className="analysis-item">
              <span>Risk Level</span>

              {loading ? (
                <strong>Analyzing...</strong>
              ) : (
                <span style={riskBadgeStyle}>
                  {riskLevel}
                </span>
              )}
            </div>

            <div className="analysis-item">
              <span>Priority</span>

              {loading ? (
                <strong>Analyzing...</strong>
              ) : (
                <span style={priorityBadgeStyle}>
                  {priority}
                </span>
              )}
            </div>
          </div>
        </div>
      </section>

      <section className="dashboard-section">
        <div className="section-header">
          <div>
            <h2>AI Risk Summary</h2>

            <p>
              Key predictive maintenance indicators for
              the selected machine.
            </p>
          </div>
        </div>

        <div className="analysis-card">
          <div className="analysis-grid">
            <div className="analysis-item">
              <span>Predicted Failure</span>

              {loading ? (
                <strong>Processing...</strong>
              ) : failureRisk ? (
                <span style={failureBadgeStyle}>
                  {predictedFailure ? 'Yes' : 'No'}
                </span>
              ) : (
                <strong>--</strong>
              )}
            </div>

            <div className="analysis-item">
              <span>Failure Risk</span>

              <strong>
                {failureRiskValue !== null
                  ? `${failureRiskValue}%`
                  : '--'}
              </strong>
            </div>

            <div className="analysis-item">
              <span>Risk Level</span>

              {loading ? (
                <strong>Processing...</strong>
              ) : recommendations ? (
                <span style={riskBadgeStyle}>
                  {riskLevel}
                </span>
              ) : (
                <strong>--</strong>
              )}
            </div>

            <div className="analysis-item">
              <span>Maintenance Priority</span>

              {loading ? (
                <strong>Processing...</strong>
              ) : recommendations ? (
                <span style={priorityBadgeStyle}>
                  {priority}
                </span>
              ) : (
                <strong>--</strong>
              )}
            </div>
          </div>
        </div>
      </section>

      <section className="dashboard-section">
        <div className="section-header">
          <div>
            <h2>Recommended Maintenance Actions</h2>

            <p>
              AI-generated actions based on the current
              machine condition.
            </p>
          </div>
        </div>

        <div className="analysis-card">
          {loading ? (
            <div className="overview-placeholder">
              <strong>
                Analyzing maintenance requirements...
              </strong>

              <p>
                Please wait while the AI backend evaluates
                the selected machine.
              </p>
            </div>
          ) : recommendations?.maintenance?.actions
              ?.length ? (
            <div className="recommendation-list">
              {recommendations.maintenance.actions.map(
                (action, index) => (
                  <div
                    key={`${action}-${index}`}
                    className="recommendation-item"
                  >
                    <span className="recommendation-number">
                      {index + 1}
                    </span>

                    <div>
                      <strong>
                        Maintenance Action {index + 1}
                      </strong>

                      <p>{action}</p>
                    </div>
                  </div>
                )
              )}
            </div>
          ) : (
            <div className="overview-placeholder">
              <strong>
                No maintenance recommendations available.
              </strong>
            </div>
          )}
        </div>
      </section>

      <section className="dashboard-section">
        <div className="section-header">
          <div>
            <h2>Sensor Analysis</h2>

            <p>
              Sensor conditions contributing to the
              maintenance assessment.
            </p>
          </div>
        </div>

        <div className="analysis-card">
          {loading ? (
            <div className="overview-placeholder">
              <strong>
                Analyzing sensor conditions...
              </strong>
            </div>
          ) : recommendations?.sensor?.length ? (
            <div className="recommendation-list">
              {recommendations.sensor.map(
                (item, index) => (
                  <div
                    key={`${item}-${index}`}
                    className="recommendation-item"
                  >
                    <span className="recommendation-number">
                      {index + 1}
                    </span>

                    <div>
                      <strong>
                        Sensor Finding {index + 1}
                      </strong>

                      <p>{item}</p>
                    </div>
                  </div>
                )
              )}
            </div>
          ) : (
            <div className="overview-placeholder">
              <strong>
                No sensor analysis available.
              </strong>
            </div>
          )}
        </div>
      </section>

      <section className="dashboard-section">
        <div className="section-header">
          <div>
            <h2>Anomaly Context</h2>

            <p>
              Additional context from the machine anomaly
              analysis.
            </p>
          </div>
        </div>

        <div className="analysis-card">
          {loading ? (
            <div className="overview-placeholder">
              <strong>
                Analyzing anomaly context...
              </strong>
            </div>
          ) : recommendations?.anomaly?.length ? (
            <div className="recommendation-list">
              {recommendations.anomaly.map(
                (item, index) => (
                  <div
                    key={`${item}-${index}`}
                    className="recommendation-item"
                  >
                    <span className="recommendation-number">
                      {index + 1}
                    </span>

                    <div>
                      <strong>
                        Anomaly Finding {index + 1}
                      </strong>

                      <p>{item}</p>
                    </div>
                  </div>
                )
              )}
            </div>
          ) : (
            <div className="overview-placeholder">
              <strong>
                No anomaly context available.
              </strong>
            </div>
          )}
        </div>
      </section>
    </div>
  );
}

export default PredictiveMaintenance;