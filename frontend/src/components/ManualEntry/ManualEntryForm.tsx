import { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { manualApi } from '../../api/endpoints';

export function ManualEntryForm() {
  const queryClient = useQueryClient();
  const [platform, setPlatform] = useState('other');
  const [text, setText] = useState('');
  const [author, setAuthor] = useState('');
  const [url, setUrl] = useState('');
  const [tags, setTags] = useState('');

  const createMutation = useMutation({
    mutationFn: manualApi.createEntry,
    onSuccess: () => {
      queryClient.invalidateQueries({ queryKey: ['posts'] });
      queryClient.invalidateQueries({ queryKey: ['stats'] });
      setPlatform('other');
      setText('');
      setAuthor('');
      setUrl('');
      setTags('');
      alert('Entry created successfully!');
    },
    onError: (error) => {
      alert('Failed to create entry: ' + error);
    },
  });

  const handleSubmit = (e: React.FormEvent) => {
    e.preventDefault();

    if (!text.trim()) {
      alert('Please enter post text');
      return;
    }

    const tagList = tags
      .split(',')
      .map((t) => t.trim())
      .filter((t) => t);

    createMutation.mutate({
      platform,
      text,
      author: author || undefined,
      url: url || undefined,
      tags: tagList.length > 0 ? tagList : undefined,
    });
  };

  return (
    <div className="space-y-6">
      <h1 className="text-3xl font-bold">Add Manual Entry</h1>

      <div className="bg-white rounded-lg shadow p-6">
        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium mb-2">Platform</label>
            <select
              value={platform}
              onChange={(e) => setPlatform(e.target.value)}
              className="w-full border rounded px-3 py-2"
            >
              <option value="facebook">Facebook</option>
              <option value="instagram">Instagram</option>
              <option value="twitter">Twitter/X</option>
              <option value="linkedin">LinkedIn</option>
              <option value="youtube">YouTube</option>
              <option value="tiktok">TikTok</option>
              <option value="other">Other</option>
            </select>
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">
              Post Text *
            </label>
            <textarea
              value={text}
              onChange={(e) => setText(e.target.value)}
              rows={4}
              className="w-full border rounded px-3 py-2"
              required
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">Author</label>
            <input
              type="text"
              value={author}
              onChange={(e) => setAuthor(e.target.value)}
              className="w-full border rounded px-3 py-2"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">URL</label>
            <input
              type="url"
              value={url}
              onChange={(e) => setUrl(e.target.value)}
              className="w-full border rounded px-3 py-2"
            />
          </div>

          <div>
            <label className="block text-sm font-medium mb-2">
              Tags (comma-separated)
            </label>
            <input
              type="text"
              value={tags}
              onChange={(e) => setTags(e.target.value)}
              placeholder="tag1, tag2, tag3"
              className="w-full border rounded px-3 py-2"
            />
          </div>

          <button
            type="submit"
            disabled={createMutation.isPending}
            className="bg-blue-500 hover:bg-blue-600 text-white px-6 py-2 rounded disabled:opacity-50"
          >
            {createMutation.isPending ? 'Creating...' : 'Create Entry'}
          </button>
        </form>
      </div>
    </div>
  );
}
