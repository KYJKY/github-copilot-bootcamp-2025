import { useState } from 'react';
import { formatDistanceToNow } from 'date-fns';
import { ko } from 'date-fns/locale';
import Button from './Button';
import { likePost, unlikePost, deletePost } from '../services/api';

const PostCard = ({ post, onDelete, userName = "anonymous" }) => {
  const [isLiked, setIsLiked] = useState(false);
  const [likeCount, setLikeCount] = useState(post.likeCount);
  const [error, setError] = useState(null);

  const handleLike = async () => {
    try {
      if (isLiked) {
        await unlikePost(post.id);
        setLikeCount(prev => prev - 1);
      } else {
        await likePost(post.id, { userName });
        setLikeCount(prev => prev + 1);
      }
      setIsLiked(!isLiked);
    } catch (error) {
      console.error('좋아요 처리 중 오류:', error);
      setError('좋아요 처리 중 오류가 발생했습니다.');
    }
  };

  const handleDelete = async () => {
    try {
      await deletePost(post.id);
      onDelete?.(post.id);
    } catch (error) {
      console.error('게시물 삭제 중 오류:', error);
      setError('게시물 삭제 중 오류가 발생했습니다.');
    }
  };

  return (
    <div className="bg-white rounded-lg shadow-md p-6 mb-4">
      <div className="flex items-center justify-between mb-4">
        <div>
          <h3 className="text-lg font-semibold text-gray-900">{post.userName}</h3>
          <p className="text-sm text-gray-500">
            {formatDistanceToNow(new Date(post.createdAt), { addSuffix: true, locale: ko })}
          </p>
        </div>
        {post.userName === userName && (
          <div className="flex space-x-2">
            <Button 
              variant="danger" 
              size="sm"
              onClick={handleDelete}
            >
              삭제
            </Button>
          </div>
        )}
      </div>

      <p className="text-gray-700 mb-4">{post.content}</p>

      <div className="flex items-center justify-between text-sm text-gray-500">
        <div className="flex space-x-4">
          <button 
            onClick={handleLike}
            className={`flex items-center space-x-1 ${isLiked ? 'text-blue-600' : ''}`}
          >
            <span>👍</span>
            <span>{likeCount}</span>
          </button>
          <div className="flex items-center space-x-1">
            <span>💬</span>
            <span>{post.commentCount}</span>
          </div>
        </div>
      </div>

      {error && (
        <p className="mt-2 text-sm text-red-600">{error}</p>
      )}
    </div>
  );
};

export default PostCard;