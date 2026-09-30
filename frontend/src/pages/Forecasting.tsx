import { useState } from 'react';

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
} from 'recharts';

import {
  getTemperatureForecast,
  type ForecastResponse,
} from '../services/api';

interface ForecastChartPoint {
  label: string;
  actual?: number;
  predicted?: number;
}

function Forecasting() {
  const [selectedMachine, setSelectedMachine] =
    useState('M-001');

  const [selectedSensor, setSelectedSensor] =
    useState('temperature');

  const [temperatureHistory, setTemperatureHistory] =
    useState<string>(
      '65.2, 66.1, 67.0, 67.8, 68.4, 69.1, 68.8, 69.5, 70.0, 69.7, 70.2, 70.5'
    );

  const [forecastResult, setForecastResult] =
    useState<ForecastResponse | null>(null);

  const [chartData, setChartData] =
    useState<ForecastChartPoint[]>([]);

  const [loading, setLoading] = useState(false);

  const [error, setError] = useState('');

  async function handleForecast() {
    setError('');
    setForecastResult(null);
    setChartData([]);

    const values = temperatureHistory
      .split(',')
      .map((value) => Number(value.trim()))
      .filter((value) => !Number.isNaN(value));

    if (values.length < 12) {
      setError(
        'Please provide at least 12 temperature readings.'
      );
      return;
    }

    if (selectedSensor !== 'temperature') {
      setError(
        'The current forecasting model supports temperature forecasting only.'
      );
      return;
    }

    setLoading(true);

    try {
      const result = await getTemperatureForecast(values);

      setForecastResult(result);

      const historyChartData: ForecastChartPoint[] =
        values.slice(-12).map((value, index) => ({
          label: `T-${11 - index}`,
          actual: value,
        }));

      historyChartData.push({
        label: 'Forecast',
        predicted: result.forecast,
      });

      setChartData(historyChartData);
    } catch (err) {
      console.error(
        'Forecasting error:',
        err
      );

      setError(
        'Unable to get forecast from FastAPI. Make sure the backend is running.'
      );
    } finally {
      setLoading(false);
    }
  }

  return (
    <div>
      <div className="page-header">
        <div>
          <h1>Forecasting</h1>

          <p>
            AI-powered sensor forecasting and future
            machine condition analysis.
          </p>
        </div>

        <div className="status-badge">
          System Online
        </div>
      </div>

      <section className="dashboard-section">
        <div className="section-header">
          <div>
            <h2>Sensor Forecasting</h2>

            <p>
              Predict future sensor behavior using the
              trained forecasting model.
            </p>
          </div>
        </div>

        <div className="forecasting-card">
          <div className="forecasting-input-section">

            <div className="forecasting-selectors">
              <div>
                <label htmlFor="machine-select">
                  Machine
                </label>

                <select
                  id="machine-select"
                  value={selectedMachine}
                  onChange={(event) => {
                    setSelectedMachine(
                      event.target.value
                    );

                    setForecastResult(null);
                    setChartData([]);
                    setError('');
                  }}
                >
                  <option value="M-001">
                    M-001 — Production Machine 01
                  </option>

                  <option value="M-002">
                    M-002 — Production Machine 02
                  </option>

                  <option value="M-003">
                    M-003 — Production Machine 03
                  </option>
                </select>
              </div>

              <div>
                <label htmlFor="sensor-select">
                  Sensor
                </label>

                <select
                  id="sensor-select"
                  value={selectedSensor}
                  onChange={(event) => {
                    setSelectedSensor(
                      event.target.value
                    );

                    setForecastResult(null);
                    setChartData([]);
                    setError('');
                  }}
                >
                  <option value="temperature">
                    Temperature
                  </option>
                </select>
              </div>
            </div>

            <div className="selected-machine-info">
              <span className="machine-id">
                SELECTED MACHINE
              </span>

              <strong>
                {selectedMachine}
              </strong>

              <span>
                Temperature forecasting enabled
              </span>
            </div>

            <label htmlFor="temperature-history">
              Recent Temperature Readings
            </label>

            <p className="input-help">
              Enter at least 12 temperature readings,
              separated by commas.
            </p>

            <textarea
              id="temperature-history"
              value={temperatureHistory}
              onChange={(event) =>
                setTemperatureHistory(
                  event.target.value
                )
              }
              rows={5}
              placeholder="65.2, 66.1, 67.0, ..."
            />

            <button
              type="button"
              onClick={handleForecast}
              disabled={loading}
              className="primary-button"
            >
              {loading
                ? 'Generating Forecast...'
                : 'Generate Forecast'}
            </button>
          </div>

          {error && (
            <div className="forecast-error">
              {error}
            </div>
          )}

          {!forecastResult && !error && (
            <div className="overview-placeholder">
              <div className="overview-icon">
                ↗
              </div>

              <div>
                <strong>
                  Forecasting Intelligence
                </strong>

                <p>
                  Select a machine, enter recent
                  temperature readings, and generate an
                  AI-powered future prediction.
                </p>
              </div>
            </div>
          )}

          {forecastResult && (
            <>
              <div className="forecast-result">
                <div className="forecast-result-header">
                  <div>
                    <span className="machine-id">
                      AI FORECAST
                    </span>

                    <h3>
                      Temperature Prediction
                    </h3>
                  </div>

                  <span className="status-badge">
                    Model Active
                  </span>
                </div>

                <div className="machine-metrics">
                  <div>
                    <span>
                      Selected Machine
                    </span>

                    <strong>
                      {selectedMachine}
                    </strong>
                  </div>

                  <div>
                    <span>
                      Forecast Sensor
                    </span>

                    <strong>
                      {forecastResult.sensor}
                    </strong>
                  </div>

                  <div>
                    <span>
                      Predicted Temperature
                    </span>

                    <strong>
                      {forecastResult.forecast} K
                    </strong>
                  </div>

                  <div>
                    <span>
                      History Points
                    </span>

                    <strong>
                      {forecastResult.history_points}
                    </strong>
                  </div>
                </div>

                <div className="machine-metrics">
                  <div>
                    <span>
                      Prediction Status
                    </span>

                    <strong>
                      Generated
                    </strong>
                  </div>

                  <div>
                    <span>
                      Model
                    </span>

                    <strong>
                      Random Forest
                    </strong>
                  </div>

                  <div>
                    <span>
                      Forecast Horizon
                    </span>

                    <strong>
                      Next Reading
                    </strong>
                  </div>

                  <div>
                    <span>
                      System Status
                    </span>

                    <strong>
                      Online
                    </strong>
                  </div>
                </div>
              </div>

              <div className="dashboard-overview">
                <div className="section-heading">
                  <div>
                    <h3>
                      Actual vs Predicted
                    </h3>

                    <p>
                      Recent temperature readings and
                      the next AI-generated prediction.
                    </p>
                  </div>
                </div>

                <div
                  style={{
                    width: '100%',
                    height: '320px',
                  }}
                >
                  <ResponsiveContainer
                    width="100%"
                    height="100%"
                  >
                    <LineChart
                      data={chartData}
                      margin={{
                        top: 10,
                        right: 20,
                        left: 10,
                        bottom: 10,
                      }}
                    >
                      <CartesianGrid
                        strokeDasharray="3 3"
                      />

                      <XAxis
                        dataKey="label"
                      />

                      <YAxis
                        domain={[
                          'auto',
                          'auto',
                        ]}
                        unit=" K"
                      />

                      <Tooltip />

                      <Line
                        type="monotone"
                        dataKey="actual"
                        name="Actual"
                        strokeWidth={2}
                        connectNulls
                        dot={{ r: 4 }}
                      />

                      <Line
                        type="monotone"
                        dataKey="predicted"
                        name="AI Forecast"
                        strokeWidth={3}
                        strokeDasharray="6 4"
                        dot={{ r: 6 }}
                      />
                    </LineChart>
                  </ResponsiveContainer>
                </div>
              </div>
            </>
          )}

          <div className="dashboard-overview">
            <div className="section-heading">
              <div>
                <h3>
                  Forecast Model Information
                </h3>

                <p>
                  Configuration and validated performance
                  of the temperature forecasting model.
                </p>
              </div>
            </div>

            <div className="machine-metrics">
              <div>
                <span>Algorithm</span>

                <strong>
                  Random Forest
                </strong>
              </div>

              <div>
                <span>Input Window</span>

                <strong>
                  12 Readings
                </strong>
              </div>

              <div>
                <span>Forecast Target</span>

                <strong>
                  Temperature
                </strong>
              </div>

              <div>
                <span>Test MAE</span>

                <strong>
                  3.89 K
                </strong>
              </div>
            </div>

            <div className="machine-metrics">
              <div>
                <span>Test RMSE</span>

                <strong>
                  4.81 K
                </strong>
              </div>

              <div>
                <span>MAE Improvement</span>

                <strong>
                  30.50%
                </strong>
              </div>

              <div>
                <span>RMSE Improvement</span>

                <strong>
                  29.70%
                </strong>
              </div>

              <div>
                <span>Model Status</span>

                <strong>
                  Validated
                </strong>
              </div>
            </div>
          </div>
        </div>
      </section>
    </div>
  );
}

export default Forecasting;