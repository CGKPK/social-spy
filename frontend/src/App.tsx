import { BrowserRouter, Routes, Route, Link } from 'react-router-dom';
import { QueryClient, QueryClientProvider } from '@tanstack/react-query';
import { Dashboard } from './components/Dashboard/Dashboard';
import { PostList } from './components/Posts/PostList';
import { MonitoringControl } from './components/Monitoring/MonitoringControl';
import { ManualEntryForm } from './components/ManualEntry/ManualEntryForm';

const queryClient = new QueryClient({
  defaultOptions: {
    queries: {
      refetchOnWindowFocus: false,
      retry: 1,
    },
  },
});

function App() {
  return (
    <QueryClientProvider client={queryClient}>
      <BrowserRouter>
        <div className="min-h-screen bg-gray-100">
          <nav className="bg-white shadow-lg">
            <div className="max-w-7xl mx-auto px-4">
              <div className="flex justify-between h-16">
                <div className="flex space-x-8">
                  <Link
                    to="/"
                    className="inline-flex items-center px-1 pt-1 border-b-2 border-transparent hover:border-blue-500 text-sm font-medium"
                  >
                    Dashboard
                  </Link>
                  <Link
                    to="/posts"
                    className="inline-flex items-center px-1 pt-1 border-b-2 border-transparent hover:border-blue-500 text-sm font-medium"
                  >
                    Posts
                  </Link>
                  <Link
                    to="/monitoring"
                    className="inline-flex items-center px-1 pt-1 border-b-2 border-transparent hover:border-blue-500 text-sm font-medium"
                  >
                    Monitoring
                  </Link>
                  <Link
                    to="/manual-entry"
                    className="inline-flex items-center px-1 pt-1 border-b-2 border-transparent hover:border-blue-500 text-sm font-medium"
                  >
                    Add Entry
                  </Link>
                </div>
              </div>
            </div>
          </nav>

          <main className="max-w-7xl mx-auto py-6 px-4">
            <Routes>
              <Route path="/" element={<Dashboard />} />
              <Route path="/posts" element={<PostList />} />
              <Route path="/monitoring" element={<MonitoringControl />} />
              <Route path="/manual-entry" element={<ManualEntryForm />} />
            </Routes>
          </main>
        </div>
      </BrowserRouter>
    </QueryClientProvider>
  );
}

export default App;
