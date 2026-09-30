import { useEffect, useState } from 'react';

import MainLayout from './components/MainLayout';
import TopHeader from './components/TopHeader';

import MachineMonitoring from './pages/MachineMonitoring';
import Anomalies from './pages/Anomalies';
import PredictiveMaintenance from './pages/PredictiveMaintenance';
import Forecasting from './pages/Forecasting';
import Copilot from './pages/Copilot';

import {
  DEFAULT_MACHINE,
  getDashboardSummary,
  getMachineStatus,
  type DashboardSummary,
  type MachineStatusResponse,
} from './services/api';


function App() {
  const [machineData, setMachineData] =
    useState<MachineStatusResponse | null>(
      null
    );

  const [dashboardSummary, setDashboardSummary] =
    useState<DashboardSummary | null>(
      null
    );

  const [backendError, setBackendError] =
    useState('');

  const [dashboardLoading, setDashboardLoading] =
    useState(true);


  useEffect(() => {
    let isMounted = true;


    async function loadMachineStatus() {
      try {
        const data =
          await getMachineStatus(
            DEFAULT_MACHINE
          );

        if (isMounted) {
          setMachineData(data);
          setBackendError('');
        }
      } catch (error) {
        console.error(
          'Machine status error:',
          error
        );

        if (isMounted) {
          setBackendError(
            'Unable to load machine data from FastAPI.'
          );
        }
      }
    }


    async function loadDashboardSummary() {
      try {
        setDashboardLoading(true);

        const data =
          await getDashboardSummary();

        if (isMounted) {
          setDashboardSummary(data);
        }
      } catch (error) {
        console.error(
          'Dashboard summary error:',
          error
        );

        if (isMounted) {
          setBackendError(
            'Unable to load dashboard summary from FastAPI.'
          );
        }
      } finally {
        if (isMounted) {
          setDashboardLoading(false);
        }
      }
    }


    loadMachineStatus();
    loadDashboardSummary();


    const refreshInterval =
      window.setInterval(
        () => {
          loadMachineStatus();
          loadDashboardSummary();
        },
        5000
      );


    return () => {
      isMounted = false;
      window.clearInterval(
        refreshInterval
      );
    };
  }, []);


  const dashboardContent = (
    <>
      <div className="dashboard-intro">
        <h2>
          Industrial Monitoring Dashboard
        </h2>

        <p>
          Monitor machine health, sensor
          conditions, anomalies, and predictive
          maintenance insights.
        </p>
      </div>


      <div className="dashboard-grid">
        <div className="dashboard-card">
          <span className="dashboard-card-label">
            Total Machines
          </span>

          <strong className="dashboard-card-value">
            {dashboardLoading
              ? '...'
              : dashboardSummary
                ?.total_machines ?? '--'}
          </strong>
        </div>


        <div className="dashboard-card">
          <span className="dashboard-card-label">
            Healthy
          </span>

          <strong className="dashboard-card-value">
            {dashboardLoading
              ? '...'
              : dashboardSummary
                ?.healthy ?? '--'}
          </strong>
        </div>


        <div className="dashboard-card">
          <span className="dashboard-card-label">
            Warnings
          </span>

          <strong className="dashboard-card-value">
            {dashboardLoading
              ? '...'
              : dashboardSummary
                ?.warning ?? '--'}
          </strong>
        </div>


        <div className="dashboard-card">
          <span className="dashboard-card-label">
            Critical
          </span>

          <strong className="dashboard-card-value">
            {dashboardLoading
              ? '...'
              : dashboardSummary
                ?.critical ?? '--'}
          </strong>
        </div>
      </div>


      <div className="dashboard-overview">
        <div className="section-heading">
          <div>
            <h3>
              System Overview
            </h3>

            <p>
              AI-powered industrial health
              monitoring.
            </p>
          </div>

          <div className="live-indicator">
            <span className="live-dot" />

            {dashboardLoading
              ? 'CONNECTING'
              : dashboardSummary
                ?.system_status ||
                'Offline'}
          </div>
        </div>


        <div className="overview-placeholder">
          <div className="overview-icon">
            AI
          </div>

          <div>
            <strong>
              Predictive Intelligence Active
            </strong>

            <p>
              Machine health is being evaluated
              using sensor data and AI-powered
              predictive analysis.
            </p>
          </div>
        </div>
      </div>


      <div className="machine-section">
        <div className="section-heading">
          <div>
            <h3>
              Machine Status
            </h3>

            <p>
              Live machine health information
              from the AI backend.
            </p>
          </div>
        </div>


        <div className="machine-grid">
          <div className="machine-card">
            <div className="machine-card-header">
              <div>
                <span className="machine-id">
                  {DEFAULT_MACHINE.machine_id}
                </span>

                <h4>
                  Production Machine 01
                </h4>
              </div>

              <span className="machine-status-normal">
                {machineData
                  ?.machine_status ||
                  'Loading...'}
              </span>
            </div>


            <div className="machine-metrics">
              <div>
                <span>
                  Process Temperature
                </span>

                <strong>
                  {machineData?.sensor_data[
                    'Process temperature [K]'
                  ] ?? '--'}{' '}
                  K
                </strong>
              </div>


              <div>
                <span>
                  Rotational Speed
                </span>

                <strong>
                  {machineData?.sensor_data[
                    'Rotational speed [rpm]'
                  ] ?? '--'}{' '}
                  rpm
                </strong>
              </div>


              <div>
                <span>
                  Torque
                </span>

                <strong>
                  {machineData?.sensor_data[
                    'Torque [Nm]'
                  ] ?? '--'}{' '}
                  Nm
                </strong>
              </div>


              <div>
                <span>
                  Tool Wear
                </span>

                <strong>
                  {machineData?.sensor_data[
                    'Tool wear [min]'
                  ] ?? '--'}{' '}
                  min
                </strong>
              </div>
            </div>
          </div>


          <div className="machine-card">
            <div className="machine-card-header">
              <div>
                <span className="machine-id">
                  M-002
                </span>

                <h4>
                  Production Machine 02
                </h4>
              </div>

              <span className="machine-status-warning">
                Warning
              </span>
            </div>


            <div className="machine-metrics">
              <div>
                <span>
                  Temperature
                </span>

                <strong>
                  81°C
                </strong>
              </div>

              <div>
                <span>
                  Vibration
                </span>

                <strong>
                  4.7 mm/s
                </strong>
              </div>

              <div>
                <span>
                  Pressure
                </span>

                <strong>
                  6.8 bar
                </strong>
              </div>

              <div>
                <span>
                  RPM
                </span>

                <strong>
                  1,842 rpm
                </strong>
              </div>
            </div>
          </div>


          <div className="machine-card">
            <div className="machine-card-header">
              <div>
                <span className="machine-id">
                  M-003
                </span>

                <h4>
                  Production Machine 03
                </h4>
              </div>

              <span className="machine-status-critical">
                Critical
              </span>
            </div>


            <div className="machine-metrics">
              <div>
                <span>
                  Temperature
                </span>

                <strong>
                  94°C
                </strong>
              </div>

              <div>
                <span>
                  Vibration
                </span>

                <strong>
                  7.8 mm/s
                </strong>
              </div>

              <div>
                <span>
                  Pressure
                </span>

                <strong>
                  8.1 bar
                </strong>
              </div>

              <div>
                <span>
                  RPM
                </span>

                <strong>
                  2,140 rpm
                </strong>
              </div>
            </div>
          </div>
        </div>
      </div>


      <div className="sensor-section">
        <div className="section-heading">
          <div>
            <h3>
              Live Sensor Monitoring
            </h3>

            <p>
              Current readings received from
              the connected machine.
            </p>
          </div>

          <div className="live-indicator">
            <span className="live-dot" />
            LIVE
          </div>
        </div>


        <div className="sensor-grid">
          <div className="sensor-card">
            <span className="sensor-icon">
              T
            </span>

            <span className="sensor-name">
              Process Temperature
            </span>

            <strong className="sensor-value">
              {machineData?.sensor_data[
                'Process temperature [K]'
              ] ?? '--'}{' '}
              K
            </strong>
          </div>


          <div className="sensor-card">
            <span className="sensor-icon">
              R
            </span>

            <span className="sensor-name">
              Rotational Speed
            </span>

            <strong className="sensor-value">
              {machineData?.sensor_data[
                'Rotational speed [rpm]'
              ] ?? '--'}{' '}
              rpm
            </strong>
          </div>


          <div className="sensor-card">
            <span className="sensor-icon">
              τ
            </span>

            <span className="sensor-name">
              Torque
            </span>

            <strong className="sensor-value">
              {machineData?.sensor_data[
                'Torque [Nm]'
              ] ?? '--'}{' '}
              Nm
            </strong>
          </div>


          <div className="sensor-card">
            <span className="sensor-icon">
              W
            </span>

            <span className="sensor-name">
              Tool Wear
            </span>

            <strong className="sensor-value">
              {machineData?.sensor_data[
                'Tool wear [min]'
              ] ?? '--'}{' '}
              min
            </strong>
          </div>
        </div>
      </div>


      <div className="dashboard-overview">
        <div className="section-heading">
          <div>
            <h3>
              AI Health Analysis
            </h3>

            <p>
              Current prediction from the
              machine-status model.
            </p>
          </div>
        </div>


        {backendError ? (
          <div className="overview-placeholder">
            <strong>
              {backendError}
            </strong>
          </div>
        ) : (
          <div className="machine-metrics">
            <div>
              <span>
                Failure Risk
              </span>

              <strong>
                {machineData?.failure_risk ??
                  '--'}
              </strong>
            </div>


            <div>
              <span>
                Predicted Failure
              </span>

              <strong>
                {machineData
                  ? machineData.predicted_failure
                    ? 'Yes'
                    : 'No'
                  : '--'}
              </strong>
            </div>


            <div>
              <span>
                Anomaly Detected
              </span>

              <strong>
                {machineData
                  ? machineData.anomaly_detected
                    ? 'Yes'
                    : 'No'
                  : '--'}
              </strong>
            </div>


            <div>
              <span>
                Anomaly Score
              </span>

              <strong>
                {machineData?.anomaly_score ??
                  '--'}
              </strong>
            </div>
          </div>
        )}
      </div>
    </>
  );


  const currentPath =
    window.location.pathname;


  return (
    <MainLayout>
      <TopHeader
        title="AI Industrial Intelligence"
        subtitle="Predictive Maintenance & Industrial Monitoring System"
      />


      {currentPath === '/machines' ? (
        <MachineMonitoring />
      ) : currentPath === '/anomalies' ? (
        <Anomalies />
      ) : currentPath === '/maintenance' ? (
        <PredictiveMaintenance />
      ) : currentPath === '/forecasting' ? (
        <Forecasting />
      ) : currentPath === '/copilot' ? (
        <Copilot />
      ) : (
        dashboardContent
      )}
    </MainLayout>
  );
}


export default App;