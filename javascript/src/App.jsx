import { useState, useEffect } from 'react'
import { getPosts } from './services/api'
import NewPostForm from './components/NewPostForm'
import PostCard from './components/PostCard'

function App() {
  const [posts, setPosts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const userName = "사용자"; // 실제 앱에서는 인증 시스템과 연동

  const fetchPosts = async () => {
    try {
      const { data } = await getPosts();
      setPosts(data);
    } catch (err) {
      setError('게시물을 불러오는 중 오류가 발생했습니다.' + err.message);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    fetchPosts();
  }, []);

  const handlePostCreated = (newPost) => {
    setPosts(prev => [newPost, ...prev]);
  };

  const handlePostDeleted = (deletedPostId) => {
    setPosts(prev => prev.filter(post => post.id !== deletedPostId));
  };

  return (
    <div className="min-h-screen bg-gray-100">
      <div className="max-w-4xl mx-auto px-4 py-8">
        {/* 헤더 */}
        <header className="text-center mb-8">
          <h1 className="text-3xl font-bold text-gray-900 mb-2">SNS 앱</h1>
          <p className="text-gray-600">친구들과 이야기를 나눠보세요</p>
        </header>

        {/* 메인 컨텐츠 */}
        <main>
          <div className="mb-8">
            <NewPostForm 
              onPostCreated={handlePostCreated}
              userName={userName}
            />
          </div>

          {/* 게시물 목록 */}
          <div className="space-y-6">
            {loading ? (
              <div className="text-center py-8">
                <div className="inline-block animate-spin rounded-full h-8 w-8 border-4 border-gray-200 border-t-blue-600"></div>
              </div>
            ) : error ? (
              <div className="bg-red-50 text-red-600 p-4 rounded-lg text-center">
                {error}
              </div>
            ) : posts.length === 0 ? (
              <div className="bg-white rounded-lg shadow-md p-8 text-center text-gray-500">
                아직 게시물이 없습니다. 첫 게시물을 작성해보세요!
              </div>
            ) : (
              posts.map(post => (
                <PostCard
                  key={post.id}
                  post={post}
                  userName={userName}
                  onDelete={handlePostDeleted}
                />
              ))
            )}
          </div>
        </main>
      </div>
    </div>
  )
}

export default App
