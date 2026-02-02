import { useState } from 'react';
import { useMonitoring } from '../../hooks/useMonitoring';

export function MonitoringControl() {
  const {
    status,
    startMonitoring,
    stopMonitoring,
    fetchNow,
    isStarting,
    isStopping,
    isFetching,
  } = useMonitoring();

  const [interval, setInterval] = useState(30);

  const isRunning = status?.status === 'running';

  const handleStart = () => {
    startMonitoring(interval);
  };

  const handleStop = () => {
    stopMonitoring();
  };

  const handleFetch = () => {
    fetchNow();
  };

  return (
    <div className="bg-white rounded-lg shadow p-6">
      <h2 className="text-2xl font-bold mb-4">Monitoring Control</h2>

      <div className="space-y-4">
        <div className="flex items-center space-x-4">
          <div className="flex items-center space-x-2">
            <span
              className={`w-3 h-3 rounded-full ${
                isRunning ? 'bg-green-500' : 'bg-gray-400'
              }`}
            ></span>
            <span className="font-medium">
              Status: {isRunning ? 'Running' : 'Stopped'}
            </span>
          </div>

          {status?.last_check && (
            <div className="text-sm text-gray-600">
              Last check: {new Date(status.last_check).toLocaleString()}
            </div>
          )}
        </div>

        {isRunning && status?.next_check_in !== undefined && (
          <div className="text-sm text-gray-600">
            Next check in: {Math.floor(status.next_check_in / 60)}m{' '}
            {status.next_check_in % 60}s
          </div>
        )}

        <div className="flex items-center space-x-4">
          <label className="font-medium">Interval (minutes):</label>
          <input
            type="number"
            min="1"
            max="1440"
            value={interval}
            onChange={(e) => setInterval(parseInt(e.target.value))}
            disabled={isRunning}
            className="border rounded px-3 py-2 w-24"
          />
        </div>

        <div className="flex space-x-4">
          {!isRunning ? (
            <button
              onClick={handleStart}
              disabled={isStarting}
              className="bg-green-500 hover:bg-green-600 text-white px-6 py-2 rounded disabled:opacity-50"
            >
              {isStarting ? 'Starting...' : 'Start Monitoring'}
            </button>
          ) : (
            <button
              onClick={handleStop}
              disabled={isStopping}
              className="bg-red-500 hover:bg-red-600 text-white px-6 py-2 rounded disabled:opacity-50"
            >
              {isStopping ? 'Stopping...' : 'Stop Monitoring'}
            </button>
          )}

          <button
            onClick={handleFetch}
            disabled={isFetching}
            className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded disabled:opacity-50"
          >
            {isFetching ? 'Fetching...' : 'Fetch Now'}
          </button>
        </div>
      </div>
    </div>
  );
}
