import { useState } from 'react';
import Button from './Button';
import { createPost } from '../services/api';

const NewPostForm = ({ onPostCreated, userName = "anonymous" }) => {
  const [content, setContent] = useState('');
  const [isSubmitting, setIsSubmitting] = useState(false);
  const [error, setError] = useState(null);

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!content.trim()) return;

    setIsSubmitting(true);
    setError(null);

    try {
      const { data } = await createPost({ content, userName });
      onPostCreated?.(data);
      setContent('');
    } catch (err) {
      setError('게시물 작성 중 오류가 발생했습니다.' + err.message);
    } finally {
      setIsSubmitting(false);
    }
  };

  return (
    <form onSubmit={handleSubmit} className="bg-white rounded-lg shadow-md p-6 mb-6">
      <div className="mb-4">
        <textarea
          value={content}
          onChange={(e) => setContent(e.target.value)}
          placeholder="무슨 생각을 하고 계신가요?"
          className="w-full min-h-[120px] p-4 border border-gray-300 rounded-lg focus:ring-2 focus:ring-blue-500 focus:border-transparent resize-none"
        />
      </div>
      
      <div className="flex items-center justify-between">
        <div className="text-sm text-gray-500">
          {userName}으로 게시됩니다
        </div>
        <Button
          type="submit"
          disabled={isSubmitting || !content.trim()}
        >
          {isSubmitting ? '게시 중...' : '게시하기'}
        </Button>
      </div>

      {error && (
        <p className="mt-2 text-sm text-red-600">{error}</p>
      )}
    </form>
  );
};

export default NewPostForm;