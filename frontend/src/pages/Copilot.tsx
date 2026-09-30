import { useState } from 'react';

import {
  DEFAULT_MACHINE,
  processCopilotQuery,
  type CopilotQueryResponse,
} from '../services/api';


function formatToolName(
  tool: string | null
): string {
  if (!tool) {
    return 'No Tool';
  }

  return tool
    .replace('get_', '')
    .replaceAll('_', ' ')
    .replace(/\b\w/g, (letter) =>
      letter.toUpperCase()
    );
}


function Copilot() {
  const [query, setQuery] = useState(
    'What is the current machine status?'
  );

  const [result, setResult] =
    useState<CopilotQueryResponse | null>(null);

  const [loading, setLoading] =
    useState(false);

  const [error, setError] =
    useState('');


  async function handleQuery() {
    const cleanQuery = query.trim();

    if (!cleanQuery) {
      setError(
        'Please enter an industrial machine question.'
      );
      return;
    }

    setLoading(true);
    setError('');
    setResult(null);

    try {
      const response =
        await processCopilotQuery(
          cleanQuery,
          DEFAULT_MACHINE
        );

      setResult(response);
    } catch (err) {
      console.error(
        'Copilot error:',
        err
      );

      setError(
        'Unable to connect to the AI Industrial Copilot. Make sure FastAPI is running.'
      );
    } finally {
      setLoading(false);
    }
  }


  function handleSuggestion(
    suggestion: string
  ) {
    setQuery(suggestion);
    setResult(null);
    setError('');
  }


  return (
    <div>
      <div className="page-header">
        <div>
          <h1>AI Industrial Copilot</h1>

          <p>
            Ask questions about machine health,
            anomalies, risk, forecasting,
            explanations, and maintenance.
          </p>
        </div>

        <div className="status-badge">
          Copilot Online
        </div>
      </div>


      <section className="dashboard-section">
        <div className="section-header">
          <div>
            <h2>Industrial Intelligence Assistant</h2>

            <p>
              Grounded in the project's verified
              machine-analysis tools and models.
            </p>
          </div>
        </div>


        <div className="forecasting-card">
          <div className="overview-placeholder">
            <div className="overview-icon">
              AI
            </div>

            <div>
              <strong>
                AI Industrial Copilot
              </strong>

              <p>
                Ask a machine-related question
                and the Copilot will route it to
                the appropriate verified analysis
                tool.
              </p>
            </div>
          </div>


          <div className="machine-section">
            <div className="section-heading">
              <div>
                <h3>
                  Ask the Copilot
                </h3>

                <p>
                  Current analysis uses machine
                  M-001 sensor conditions.
                </p>
              </div>
            </div>


            <textarea
              value={query}
              onChange={(event) => {
                setQuery(
                  event.target.value
                );
                setError('');
              }}
              rows={5}
              placeholder="Ask about machine status, failure risk, anomalies, forecasting, explanation, or maintenance..."
            />


            <button
              type="button"
              className="primary-button"
              onClick={handleQuery}
              disabled={loading}
            >
              {loading
                ? 'Analyzing...'
                : 'Ask Copilot'}
            </button>


            <div className="machine-metrics">
              <div>
                <span>
                  Machine
                </span>

                <strong>
                  {DEFAULT_MACHINE.machine_id}
                </strong>
              </div>

              <div>
                <span>
                  Air Temperature
                </span>

                <strong>
                  {DEFAULT_MACHINE.air_temperature}
                  {' '}K
                </strong>
              </div>

              <div>
                <span>
                  Process Temperature
                </span>

                <strong>
                  {DEFAULT_MACHINE.process_temperature}
                  {' '}K
                </strong>
              </div>

              <div>
                <span>
                  Rotational Speed
                </span>

                <strong>
                  {DEFAULT_MACHINE.rotational_speed}
                  {' '}rpm
                </strong>
              </div>
            </div>
          </div>


          <div className="dashboard-overview">
            <div className="section-heading">
              <div>
                <h3>
                  Example Questions
                </h3>

                <p>
                  Select a question to test the
                  Copilot quickly.
                </p>
              </div>
            </div>


            <div className="machine-metrics">
              <button
                type="button"
                className="primary-button"
                onClick={() =>
                  handleSuggestion(
                    'What is the current machine status?'
                  )
                }
              >
                Machine Status
              </button>

              <button
                type="button"
                className="primary-button"
                onClick={() =>
                  handleSuggestion(
                    'What is the failure risk?'
                  )
                }
              >
                Failure Risk
              </button>

              <button
                type="button"
                className="primary-button"
                onClick={() =>
                  handleSuggestion(
                    'Are there any recent anomalies?'
                  )
                }
              >
                Anomalies
              </button>

              <button
                type="button"
                className="primary-button"
                onClick={() =>
                  handleSuggestion(
                    'Explain the prediction.'
                  )
                }
              >
                Explain
              </button>
            </div>


            <div className="machine-metrics">
              <button
                type="button"
                className="primary-button"
                onClick={() =>
                  handleSuggestion(
                    'What is the temperature forecast?'
                  )
                }
              >
                Forecast
              </button>

              <button
                type="button"
                className="primary-button"
                onClick={() =>
                  handleSuggestion(
                    'What maintenance actions are recommended?'
                  )
                }
              >
                Maintenance
              </button>

              <button
                type="button"
                className="primary-button"
                onClick={() =>
                  handleSuggestion(
                    'Show me the recent machine history.'
                  )
                }
              >
                History
              </button>
            </div>
          </div>


          {error && (
            <div className="forecast-error">
              {error}
            </div>
          )}


          {result && (
            <div className="dashboard-overview">
              <div className="section-heading">
                <div>
                  <h3>
                    Copilot Response
                  </h3>

                  <p>
                    Verified result returned from
                    the selected backend tool.
                  </p>
                </div>

                <span className="status-badge">
                  {result.copilot.success
                    ? 'Verified'
                    : 'Not Resolved'}
                </span>
              </div>


              <div className="selected-machine-info">
                <span className="machine-id">
                  USER QUERY
                </span>

                <strong>
                  {result.query}
                </strong>

                <span>
                  Tool:{' '}
                  {formatToolName(
                    result.copilot.tool
                  )}
                </span>
              </div>


              {result.copilot.result && (
                <div className="machine-metrics">
                  {result.copilot.result
                    .machine_status !==
                    undefined && (
                    <div>
                      <span>
                        Machine Status
                      </span>

                      <strong>
                        {
                          result.copilot.result
                            .machine_status
                        }
                      </strong>
                    </div>
                  )}


                  {result.copilot.result
                    .failure_risk !==
                    undefined && (
                    <div>
                      <span>
                        Failure Risk
                      </span>

                      <strong>
                        {
                          result.copilot.result
                            .failure_risk
                        }
                      </strong>
                    </div>
                  )}


                  {result.copilot.result
                    .predicted_failure !==
                    undefined && (
                    <div>
                      <span>
                        Predicted Failure
                      </span>

                      <strong>
                        {
                          result.copilot.result
                            .predicted_failure
                            ? 'Yes'
                            : 'No'
                        }
                      </strong>
                    </div>
                  )}


                  {result.copilot.result
                    .anomaly_detected !==
                    undefined && (
                    <div>
                      <span>
                        Anomaly
                      </span>

                      <strong>
                        {
                          result.copilot.result
                            .anomaly_detected
                            ? 'Detected'
                            : 'None'
                        }
                      </strong>
                    </div>
                  )}


                  {result.copilot.result
                    .forecast !==
                    undefined && (
                    <div>
                      <span>
                        Forecast
                      </span>

                      <strong>
                        {
                          result.copilot.result
                            .forecast
                        }{' '}
                        K
                      </strong>
                    </div>
                  )}
                </div>
              )}


              <div className="overview-placeholder">
                <div>
                  <strong>
                    Backend Tool Result
                  </strong>

                  <pre
                    style={{
                      whiteSpace:
                        'pre-wrap',
                      marginTop:
                        '12px',
                    }}
                  >
                    {JSON.stringify(
                      result.copilot.result ??
                        result.copilot.message,
                      null,
                      2
                    )}
                  </pre>
                </div>
              </div>
            </div>
          )}
        </div>
      </section>
    </div>
  );
}


export default Copilot;