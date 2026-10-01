const API_BASE_URL =
  import.meta.env.VITE_API_URL ||
  'https://ai-industrial-intelligence-06.onrender.com';


export interface MachineStatusRequest {
  machine_id: string;
  air_temperature: number;
  process_temperature: number;
  rotational_speed: number;
  torque: number;
  tool_wear: number;
}


export interface MachineStatusResponse {
  machine_status: string;
  failure_risk: number;
  predicted_failure: boolean;
  anomaly_detected: boolean;
  anomaly_score: number;
  sensor_data: {
    'Air temperature [K]': number;
    'Process temperature [K]': number;
    'Rotational speed [rpm]': number;
    'Torque [Nm]': number;
    'Tool wear [min]': number;
  };
}


export interface FailureRiskResponse {
  failure_risk: number;
  predicted_failure: boolean;
}


export interface AnomalyResponse {
  anomaly_detected: boolean;
  anomaly_score: number;
}


export interface ForecastRequest {
  temperature_history: number[];
}


export interface ForecastResponse {
  sensor: string;
  forecast: number;
  history_points: number;
}


export interface MaintenanceRecommendationResponse {
  risk_level: string;
  maintenance: {
    priority: string;
    actions: string[];
  };
  sensor: string[];
  anomaly: string[];
}


export interface MachineHistoryPoint {
  time: string;
  temperature: number;
  vibration: number;
  pressure: number;
  rpm: number;
}


export interface DashboardSummary {
  total_machines: number;
  healthy: number;
  warning: number;
  critical: number;
  system_status: string;
}


export interface CopilotQueryResponse {
  query: string;
  copilot: {
    success: boolean;
    tool: string | null;
    result?: any;
    message?: string;
  };
}


export const DEFAULT_MACHINE: MachineStatusRequest = {
  machine_id: 'M-001',
  air_temperature: 298.1,
  process_temperature: 308.6,
  rotational_speed: 1500,
  torque: 40.0,
  tool_wear: 10.0,
};


export const MACHINE_PROFILES: Record<
  string,
  MachineStatusRequest
> = {
  'M-001': {
    machine_id: 'M-001',
    air_temperature: 298.1,
    process_temperature: 308.6,
    rotational_speed: 1500,
    torque: 40.0,
    tool_wear: 10.0,
  },

  'M-002': {
    machine_id: 'M-002',
    air_temperature: 301.5,
    process_temperature: 312.0,
    rotational_speed: 1450,
    torque: 48.0,
    tool_wear: 100.0,
  },

  'M-003': {
    machine_id: 'M-003',
    air_temperature: 304.5,
    process_temperature: 318.5,
    rotational_speed: 1200,
    torque: 65.0,
    tool_wear: 200.0,
  },
};


export async function checkBackendHealth() {
  const response = await fetch(
    `${API_BASE_URL}/health`
  );

  if (!response.ok) {
    throw new Error(
      'Backend health check failed.'
    );
  }

  return response.json();
}


export async function getMachineStatus(
  data: MachineStatusRequest
): Promise<MachineStatusResponse> {
  const response = await fetch(
    `${API_BASE_URL}/machine/status`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    }
  );

  if (!response.ok) {
    throw new Error(
      'Machine status request failed.'
    );
  }

  return response.json();
}


export async function getMachineFailureRisk(
  data: MachineStatusRequest
): Promise<FailureRiskResponse> {
  const response = await fetch(
    `${API_BASE_URL}/machine/failure-risk`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    }
  );

  if (!response.ok) {
    throw new Error(
      'Machine failure-risk request failed.'
    );
  }

  return response.json();
}


export async function getMachineAnomaly(
  data: MachineStatusRequest
): Promise<AnomalyResponse> {
  const response = await fetch(
    `${API_BASE_URL}/machine/anomaly`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    }
  );

  if (!response.ok) {
    throw new Error(
      'Machine anomaly request failed.'
    );
  }

  return response.json();
}


export async function getTemperatureForecast(
  temperatureHistory: number[]
): Promise<ForecastResponse> {
  const response = await fetch(
    `${API_BASE_URL}/machine/forecast`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        temperature_history:
          temperatureHistory,
      }),
    }
  );

  if (!response.ok) {
    throw new Error(
      'Temperature forecast request failed.'
    );
  }

  return response.json();
}


export async function getMaintenanceRecommendations(
  data: MachineStatusRequest
): Promise<MaintenanceRecommendationResponse> {
  const response = await fetch(
    `${API_BASE_URL}/machine/recommendations`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    }
  );

  if (!response.ok) {
    throw new Error(
      'Maintenance recommendation request failed.'
    );
  }

  return response.json();
}


export async function getMachineRecommendations(
  data: MachineStatusRequest
): Promise<MaintenanceRecommendationResponse> {
  const response = await fetch(
    `${API_BASE_URL}/machine/recommendations`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify(data),
    }
  );

  if (!response.ok) {
    throw new Error(
      'Machine recommendation request failed.'
    );
  }

  return response.json();
}


export function getMachineHistory():
  MachineHistoryPoint[] {
  return [
    {
      time: '10:00',
      temperature: 76.2,
      vibration: 3.1,
      pressure: 6.4,
      rpm: 1480,
    },
    {
      time: '10:05',
      temperature: 77.1,
      vibration: 3.3,
      pressure: 6.5,
      rpm: 1492,
    },
    {
      time: '10:10',
      temperature: 78.4,
      vibration: 3.6,
      pressure: 6.6,
      rpm: 1501,
    },
    {
      time: '10:15',
      temperature: 79.2,
      vibration: 3.9,
      pressure: 6.7,
      rpm: 1510,
    },
    {
      time: '10:20',
      temperature: 80.1,
      vibration: 4.2,
      pressure: 6.8,
      rpm: 1520,
    },
    {
      time: '10:25',
      temperature: 81.0,
      vibration: 4.7,
      pressure: 6.8,
      rpm: 1500,
    },
  ];
}


export async function getDashboardSummary():
  Promise<DashboardSummary> {
  const response = await fetch(
    `${API_BASE_URL}/dashboard/summary`
  );

  if (!response.ok) {
    throw new Error(
      'Dashboard summary request failed.'
    );
  }

  return response.json();
}


export async function processCopilotQuery(
  query: string,
  sensorData: MachineStatusRequest
): Promise<CopilotQueryResponse> {
  const response = await fetch(
    `${API_BASE_URL}/machine/copilot/query`,
    {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
      },
      body: JSON.stringify({
        query,
        sensor_data: {
          air_temperature:
            sensorData.air_temperature,

          process_temperature:
            sensorData.process_temperature,

          rotational_speed:
            sensorData.rotational_speed,

          torque:
            sensorData.torque,

          tool_wear:
            sensorData.tool_wear,

          machine_type: 'M',
        },
      }),
    }
  );

  if (!response.ok) {
    throw new Error(
      'Copilot query request failed.'
    );
  }

  return response.json();
}