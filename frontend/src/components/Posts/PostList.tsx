import { useState } from 'react';
import { usePosts } from '../../hooks/usePosts';

export function PostList() {
  const [platform, setPlatform] = useState<string>('');
  const [limit, setLimit] = useState(50);
  const [offset, setOffset] = useState(0);

  const { data, isLoading } = usePosts({
    platform: platform || undefined,
    limit,
    offset,
  });

  const handlePrevious = () => {
    setOffset(Math.max(0, offset - limit));
  };

  const handleNext = () => {
    if (data && offset + limit < data.total) {
      setOffset(offset + limit);
    }
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Posts</h1>

      {/* Filters */}
      <div className="bg-white rounded-lg shadow p-6">
        <div className="flex space-x-4">
          <div>
            <label className="block text-sm font-medium mb-2">Platform</label>
            <select
              value={platform}
              onChange={(e) => {
                setPlatform(e.target.value);
                setOffset(0);
              }}
              className="border rounded px-3 py-2"
            >
              <option value="">All Platforms</option>
              <option value="youtube">YouTube</option>
              <option value="twitter">Twitter/X</option>
              <option value="meta">Meta</option>
              <option value="linkedin">LinkedIn</option>
              <option value="manual">Manual</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Per Page</label>
            <select
              value={limit}
              onChange={(e) => {
                setLimit(parseInt(e.target.value));
                setOffset(0);
              }}
              className="border rounded px-3 py-2"
            >
              <option value="25">25</option>
              <option value="50">50</option>
              <option value="100">100</option>
            </select>
          </div>
        </div>
      </div>

      {/* Posts List */}
      {isLoading ? (
        <div>Loading posts...</div>
      ) : (
        <>
          <div className="space-y-4">
            {data?.posts.map((post: any) => (
              <div key={post.id} className="bg-white rounded-lg shadow p-6">
                <div className="flex justify-between items-start mb-2">
                  <div>
                    <span className="inline-block px-2 py-1 text-xs font-semibold rounded bg-blue-100 text-blue-800">
                      {post.platform}
                    </span>
                    {post.type && (
                      <span className="ml-2 text-xs text-gray-500">
                        {post.type}
                      </span>
                    )}
                  </div>
                  <div className="text-sm text-gray-500">
                    {post.published
                      ? new Date(post.published).toLocaleDateString()
                      : ''}
                  </div>
                </div>

                {post.author && (
                  <div className="font-semibold mb-2">{post.author}</div>
                )}

                {post.text && (
                  <div className="text-gray-700 mb-3">
                    {post.text.substring(0, 300)}
                    {post.text.length > 300 ? '...' : ''}
                  </div>
                )}

                {post.url && (
                  <a
                    href={post.url}
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-500 hover:underline text-sm"
                  >
                    View Post
                  </a>
                )}

                <div className="mt-3 flex space-x-4 text-sm text-gray-600">
                  {post.likes > 0 && <span>👍 {post.likes}</span>}
                  {post.comments > 0 && <span>💬 {post.comments}</span>}
                  {(post.shares > 0 || post.retweets > 0) && (
                    <span>🔄 {post.shares || post.retweets}</span>
                  )}
                  {post.views > 0 && <span>👁️ {post.views}</span>}
                </div>
              </div>
            ))}
          </div>

          {/* Pagination */}
          {data && data.total > 0 && (
            <div className="bg-white rounded-lg shadow p-4 flex justify-between items-center">
              <div className="text-sm text-gray-600">
                Showing {offset + 1} - {Math.min(offset + limit, data.total)} of{' '}
                {data.total}
              </div>
              <div className="flex space-x-2">
                <button
                  onClick={handlePrevious}
                  disabled={offset === 0}
                  className="px-4 py-2 border rounded disabled:opacity-50"
                >
                  Previous
                </button>
                <button
                  onClick={handleNext}
                  disabled={offset + limit >= data.total}
                  className="px-4 py-2 border rounded disabled:opacity-50"
                >
                  Next
                </button>
              </div>
            </div>
          )}
        </>
      )}
    </div>
  );
}
