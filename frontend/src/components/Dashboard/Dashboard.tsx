import { useStats } from '../../hooks/usePosts';
import { PieChart, Pie, Cell, ResponsiveContainer, Legend, Tooltip } from 'recharts';

const COLORS = ['#0088FE', '#00C49F', '#FFBB28', '#FF8042', '#8884D8'];

export function Dashboard() {
  const { data: stats, isLoading } = useStats();

  if (isLoading) {
    return <div>Loading...</div>;
  }

  const platformData = Object.entries(stats?.by_platform || {}).map(
    ([name, value]) => ({
      name,
      value,
    })
  );

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Dashboard</h1>

      {/* Stats Cards */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-sm text-gray-600">Total Posts</div>
          <div className="text-3xl font-bold">{stats?.total_posts || 0}</div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-sm text-gray-600">Total Likes</div>
          <div className="text-3xl font-bold">{stats?.total_likes || 0}</div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-sm text-gray-600">Total Comments</div>
          <div className="text-3xl font-bold">{stats?.total_comments || 0}</div>
        </div>

        <div className="bg-white rounded-lg shadow p-6">
          <div className="text-sm text-gray-600">Total Shares</div>
          <div className="text-3xl font-bold">{stats?.total_shares || 0}</div>
        </div>
      </div>

      {/* Platform Distribution */}
      {platformData.length > 0 && (
        <div className="bg-white rounded-lg shadow p-6">
          <h2 className="text-xl font-bold mb-4">Platform Distribution</h2>
          <ResponsiveContainer width="100%" height={300}>
            <PieChart>
              <Pie
                data={platformData}
                cx="50%"
                cy="50%"
                labelLine={false}
                label={({ name, percent }) =>
                  `${name}: ${(percent * 100).toFixed(0)}%`
                }
                outerRadius={80}
                fill="#8884d8"
                dataKey="value"
              >
                {platformData.map((entry, index) => (
                  <Cell
                    key={`cell-${index}`}
                    fill={COLORS[index % COLORS.length]}
                  />
                ))}
              </Pie>
              <Tooltip />
              <Legend />
            </PieChart>
          </ResponsiveContainer>
        </div>
      )}

      {stats?.last_updated && (
        <div className="text-sm text-gray-600">
          Last updated: {new Date(stats.last_updated).toLocaleString()}
        </div>
      )}
    </div>
  );
}
