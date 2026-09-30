import { useEffect, useState } from 'react';

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  Legend,
  ResponsiveContainer,
} from 'recharts';

import {
  MACHINE_PROFILES,
  getMachineAnomaly,
  getMachineHistory,
  getMachineStatus,
  getMaintenanceRecommendations,
  type AnomalyResponse,
  type MachineHistoryPoint,
  type MachineStatusResponse,
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

function MachineMonitoring() {
  const [selectedMachine, setSelectedMachine] = useState('M-001');

  const [machineStatuses, setMachineStatuses] = useState<
    Record<string, string>
  >({});

  const [machineStatus, setMachineStatus] =
    useState<MachineStatusResponse | null>(null);

  const [anomaly, setAnomaly] =
    useState<AnomalyResponse | null>(null);

  const [recommendations, setRecommendations] =
    useState<MaintenanceRecommendationResponse | null>(null);

  const [history, setHistory] =
    useState<MachineHistoryPoint[]>([]);

  const [loading, setLoading] = useState(true);

  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    setHistory(getMachineHistory());
  }, []);

  useEffect(() => {
    let mounted = true;

    const loadMachineData = async () => {
      try {
        if (mounted) {
          setLoading(true);
          setError(null);
        }

        // --------------------------------------------------
        // 1. Get profiles for ALL machines
        // --------------------------------------------------

        const machineProfiles = MACHINES.map((machine) => {
          const profile = MACHINE_PROFILES[machine.id];

          if (!profile) {
            throw new Error(
              `No sensor profile found for ${machine.id}.`
            );
          }

          return profile;
        });

        // --------------------------------------------------
        // 2. Get status for ALL machines
        // --------------------------------------------------

        const statusResponses = await Promise.all(
          machineProfiles.map((profile) =>
            getMachineStatus(profile)
          )
        );

        if (!mounted) {
          return;
        }

        // --------------------------------------------------
        // 3. Build status map for the three machine cards
        // --------------------------------------------------

        const updatedStatuses: Record<string, string> = {};

        MACHINES.forEach((machine, index) => {
          updatedStatuses[machine.id] =
            statusResponses[index].machine_status;
        });

        setMachineStatuses(updatedStatuses);

        // --------------------------------------------------
        // 4. Get selected machine profile
        // --------------------------------------------------

        const selectedProfile =
          MACHINE_PROFILES[selectedMachine];

        if (!selectedProfile) {
          throw new Error(
            `No sensor profile found for ${selectedMachine}.`
          );
        }

        // --------------------------------------------------
        // 5. Find selected machine's already-fetched status
        // --------------------------------------------------

        const selectedMachineIndex =
          MACHINES.findIndex(
            (machine) => machine.id === selectedMachine
          );

        if (selectedMachineIndex === -1) {
          throw new Error(
            `Machine ${selectedMachine} was not found.`
          );
        }

        const selectedStatus =
          statusResponses[selectedMachineIndex];

        // --------------------------------------------------
        // 6. Get detailed AI analysis for selected machine
        // --------------------------------------------------

        const [
          anomalyResponse,
          recommendationResponse,
        ] = await Promise.all([
          getMachineAnomaly(selectedProfile),
          getMaintenanceRecommendations(selectedProfile),
        ]);

        if (!mounted) {
          return;
        }

        // --------------------------------------------------
        // 7. Update selected machine details
        // --------------------------------------------------

        setMachineStatus(selectedStatus);
        setAnomaly(anomalyResponse);
        setRecommendations(recommendationResponse);

      } catch (err) {
        if (!mounted) {
          return;
        }

        setError(
          err instanceof Error
            ? err.message
            : 'Unable to load machine data.'
        );
      } finally {
        if (mounted) {
          setLoading(false);
        }
      }
    };

    // Initial load
    loadMachineData();

    // Refresh every 5 seconds
    const interval = window.setInterval(
      loadMachineData,
      5000
    );

    return () => {
      mounted = false;
      window.clearInterval(interval);
    };
  }, [selectedMachine]);

  const sensorData = machineStatus?.sensor_data;

  const latestHistory =
    history.length > 0
      ? history[history.length - 1]
      : null;

  const getStatusClass = (status?: string) => {
    if (!status) {
      return 'unknown';
    }

    return status.toLowerCase();
  };

  return (
    <div className="page-container">

      {/* Page Header */}
      <div className="page-header">

        <div>
          <h1>Machine Monitoring</h1>

          <p>
            Real-time industrial machine health,
            sensor monitoring and AI analysis.
          </p>
        </div>

        <div className="status-badge">
          <span className="status-dot" />
          System Online
        </div>

      </div>


      {/* Machine Selection */}
      <section className="section-card">

        <div className="section-header">

          <div>
            <h2>Machines</h2>

            <p>
              Select a machine to view its live
              condition and AI analysis.
            </p>
          </div>

        </div>


        <div className="machine-grid">

          {MACHINES.map((machine) => {

            const status =
              machineStatuses[machine.id];

            return (

              <button
                key={machine.id}
                type="button"
                className={`machine-card ${
                  selectedMachine === machine.id
                    ? 'active'
                    : ''
                }`}
                onClick={() =>
                  setSelectedMachine(machine.id)
                }
              >

                <div className="machine-card-top">

                  <div>
                    <span className="machine-id">
                      {machine.id}
                    </span>

                    <h3>{machine.name}</h3>
                  </div>

                  <span
                    className={`machine-status ${getStatusClass(
                      status
                    )}`}
                  >
                    {status ?? 'Loading'}
                  </span>

                </div>

              </button>

            );
          })}

        </div>

      </section>


      {/* Error */}
      {error && (
        <div className="error-message">

          <strong>Connection Error</strong>

          <p>{error}</p>

        </div>
      )}


      {/* Machine Details */}
      <section className="section-card">

        <div className="section-header">

          <div>

            <span className="section-label">
              LIVE MONITORING
            </span>

            <h2>
              Machine Details — {selectedMachine}
            </h2>

            <p>
              Current sensor readings from the AI
              monitoring system.
            </p>

          </div>

          <div className="live-indicator">
            <span className="live-dot" />
            LIVE
          </div>

        </div>


        <div className="sensor-grid">

          <div className="sensor-card">

            <span>Process Temperature</span>

            <strong>
              {sensorData
                ? sensorData[
                    'Process temperature [K]'
                  ].toFixed(1)
                : '—'}

              <small> K</small>
            </strong>

          </div>


          <div className="sensor-card">

            <span>Rotational Speed</span>

            <strong>
              {sensorData
                ? sensorData[
                    'Rotational speed [rpm]'
                  ].toFixed(0)
                : '—'}

              <small> rpm</small>
            </strong>

          </div>


          <div className="sensor-card">

            <span>Torque</span>

            <strong>
              {sensorData
                ? sensorData['Torque [Nm]'].toFixed(1)
                : '—'}

              <small> Nm</small>
            </strong>

          </div>


          <div className="sensor-card">

            <span>Tool Wear</span>

            <strong>
              {sensorData
                ? sensorData[
                    'Tool wear [min]'
                  ].toFixed(0)
                : '—'}

              <small> min</small>
            </strong>

          </div>

        </div>

      </section>


      {/* AI Health Analysis */}
      <section className="section-card">

        <div className="section-header">

          <div>

            <span className="section-label">
              AI ANALYSIS
            </span>

            <h2>AI Health Analysis</h2>

            <p>
              Machine condition evaluated by the
              predictive maintenance backend.
            </p>

          </div>

        </div>


        {loading ? (

          <div className="loading-state">
            Analyzing machine condition...
          </div>

        ) : machineStatus ? (

          <div className="analysis-grid">

            <div className="analysis-item">
              <span>Machine Status</span>

              <strong>
                {machineStatus.machine_status}
              </strong>
            </div>


            <div className="analysis-item">
              <span>Failure Risk</span>

              <strong>
                {machineStatus.failure_risk}%
              </strong>
            </div>


            <div className="analysis-item">
              <span>Predicted Failure</span>

              <strong>
                {machineStatus.predicted_failure
                  ? 'Yes'
                  : 'No'}
              </strong>
            </div>


            <div className="analysis-item">
              <span>Anomaly Detected</span>

              <strong>
                {machineStatus.anomaly_detected
                  ? 'Yes'
                  : 'No'}
              </strong>
            </div>


            <div className="analysis-item">
              <span>Anomaly Score</span>

              <strong>
                {machineStatus.anomaly_score}
              </strong>
            </div>

          </div>

        ) : (

          <div className="empty-state">
            No machine analysis available.
          </div>

        )}

      </section>


      {/* Anomaly Analysis */}
      <section className="section-card">

        <div className="section-header">

          <div>

            <span className="section-label">
              ANOMALY DETECTION
            </span>

            <h2>Anomaly Analysis</h2>

            <p>
              AI-based detection of unusual machine
              behavior.
            </p>

          </div>

        </div>


        {anomaly ? (

          <div className="analysis-grid">

            <div className="analysis-item">
              <span>Behavior</span>

              <strong>
                {anomaly.anomaly_detected
                  ? 'Abnormal Behavior'
                  : 'Normal Behavior'}
              </strong>
            </div>


            <div className="analysis-item">
              <span>Detection Status</span>

              <strong>
                {anomaly.anomaly_detected
                  ? 'Anomaly Detected'
                  : 'Normal'}
              </strong>
            </div>


            <div className="analysis-item">
              <span>Anomaly Score</span>

              <strong>
                {anomaly.anomaly_score}
              </strong>
            </div>


            <div className="analysis-item">
              <span>Machine</span>

              <strong>
                {selectedMachine}
              </strong>
            </div>

          </div>

        ) : (

          <div className="empty-state">
            No anomaly analysis available.
          </div>

        )}

      </section>


      {/* Machine History & Sensor Trend */}
      <section className="section-card">

        <div className="section-header">

          <div>

            <span className="section-label">
              SENSOR HISTORY
            </span>

            <h2>Machine History & Sensor Trend</h2>

            <p>
              Recent temperature and vibration behavior
              for the selected machine.
            </p>

          </div>


          {latestHistory && (
            <div className="history-latest">
              Latest: {latestHistory.time}
            </div>
          )}

        </div>


        {history.length > 0 ? (

          <>

            {/* Temperature Chart */}
            <div className="sensor-chart-section">

              <div className="chart-header">

                <div>
                  <h3>Temperature Trend</h3>

                  <p>
                    Recent process temperature changes.
                  </p>
                </div>

                <span className="chart-unit">
                  °C
                </span>

              </div>


              <div
                className="sensor-chart"
                style={{
                  width: '100%',
                  height: 320,
                }}
              >

                <ResponsiveContainer
                  width="100%"
                  height="100%"
                >

                  <LineChart
                    data={history}
                    margin={{
                      top: 10,
                      right: 20,
                      left: 0,
                      bottom: 5,
                    }}
                  >

                    <CartesianGrid
                      strokeDasharray="3 3"
                    />

                    <XAxis
                      dataKey="time"
                    />

                    <YAxis />

                    <Tooltip />

                    <Legend />

                    <Line
                      type="monotone"
                      dataKey="temperature"
                      name="Temperature"
                      strokeWidth={3}
                      dot={{ r: 4 }}
                      activeDot={{ r: 6 }}
                    />

                  </LineChart>

                </ResponsiveContainer>

              </div>

            </div>


            {/* Vibration Chart */}
            <div className="sensor-chart-section">

              <div className="chart-header">

                <div>
                  <h3>Vibration Trend</h3>

                  <p>
                    Recent machine vibration behavior.
                  </p>
                </div>

                <span className="chart-unit">
                  mm/s
                </span>

              </div>


              <div
                className="sensor-chart"
                style={{
                  width: '100%',
                  height: 320,
                }}
              >

                <ResponsiveContainer
                  width="100%"
                  height="100%"
                >

                  <LineChart
                    data={history}
                    margin={{
                      top: 10,
                      right: 20,
                      left: 0,
                      bottom: 5,
                    }}
                  >

                    <CartesianGrid
                      strokeDasharray="3 3"
                    />

                    <XAxis
                      dataKey="time"
                    />

                    <YAxis />

                    <Tooltip />

                    <Legend />

                    <Line
                      type="monotone"
                      dataKey="vibration"
                      name="Vibration"
                      strokeWidth={3}
                      dot={{ r: 4 }}
                      activeDot={{ r: 6 }}
                    />

                  </LineChart>

                </ResponsiveContainer>

              </div>

            </div>


            {/* Historical Data Table */}
            <div className="history-table-wrapper">

              <h3>Historical Sensor Readings</h3>

              <table className="history-table">

                <thead>

                  <tr>
                    <th>Time</th>
                    <th>Temperature</th>
                    <th>Vibration</th>
                    <th>Pressure</th>
                    <th>RPM</th>
                  </tr>

                </thead>


                <tbody>

                  {history.map((point) => (

                    <tr key={point.time}>

                      <td>{point.time}</td>

                      <td>
                        {point.temperature.toFixed(1)} °C
                      </td>

                      <td>
                        {point.vibration.toFixed(1)} mm/s
                      </td>

                      <td>
                        {point.pressure.toFixed(1)} bar
                      </td>

                      <td>
                        {point.rpm.toFixed(0)} rpm
                      </td>

                    </tr>

                  ))}

                </tbody>

              </table>

            </div>

          </>

        ) : (

          <div className="empty-state">
            No historical sensor data available.
          </div>

        )}

      </section>


      {/* Maintenance Recommendations */}
      <section className="section-card">

        <div className="section-header">

          <div>

            <span className="section-label">
              MAINTENANCE INTELLIGENCE
            </span>

            <h2>Maintenance Recommendations</h2>

            <p>
              AI-generated maintenance guidance based
              on current machine conditions.
            </p>

          </div>

        </div>


        {recommendations ? (

          <div className="maintenance-recommendations-section">

            <div className="maintenance-summary">

              <div className="maintenance-priority">

                <span>Priority</span>

                <strong>
                  {recommendations.maintenance.priority}
                </strong>

              </div>


              <div>

                <span>Risk Level</span>

                <strong>
                  {recommendations.risk_level}
                </strong>

              </div>

            </div>


            <div className="maintenance-actions">

              <h3>Recommended Actions</h3>

              <ul>

                {recommendations.maintenance.actions.map(
                  (action, index) => (

                    <li key={index}>
                      {action}
                    </li>

                  )
                )}

              </ul>

            </div>


            <div className="maintenance-context-grid">

              <div>

                <h3>Sensor Analysis</h3>

                <ul>

                  {recommendations.sensor.map(
                    (item, index) => (

                      <li key={index}>
                        {item}
                      </li>

                    )
                  )}

                </ul>

              </div>


              <div>

                <h3>Anomaly Context</h3>

                <ul>

                  {recommendations.anomaly.map(
                    (item, index) => (

                      <li key={index}>
                        {item}
                      </li>

                    )
                  )}

                </ul>

              </div>

            </div>

          </div>

        ) : (

          <div className="empty-state">
            No maintenance recommendations available.
          </div>

        )}

      </section>


      {/* Monitoring Footer */}
      <div className="monitoring-footer">

        <span>
          Monitoring updates automatically every 5 seconds.
        </span>

        <span>
          Backend: FastAPI
        </span>

      </div>

    </div>
  );
}

export default MachineMonitoring;