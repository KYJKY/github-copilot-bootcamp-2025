import axios from 'axios';

const api = axios.create({
  baseURL: 'http://localhost:8000/api',
});

export const getPosts = () => api.get('/posts');
export const getPost = (id) => api.get(`/posts/${id}`);
export const createPost = (data) => api.post('/posts', data);
export const updatePost = (id, data) => api.patch(`/posts/${id}`, data);
export const deletePost = (id) => api.delete(`/posts/${id}`);

export const getComments = (postId) => api.get(`/posts/${postId}/comments`);
export const createComment = (postId, data) => api.post(`/posts/${postId}/comments`, data);
export const updateComment = (postId, commentId, data) => 
  api.patch(`/posts/${postId}/comments/${commentId}`, data);
export const deleteComment = (postId, commentId) => 
  api.delete(`/posts/${postId}/comments/${commentId}`);

export const likePost = (postId, data) => api.post(`/posts/${postId}/likes`, data);
export const unlikePost = (postId) => api.delete(`/posts/${postId}/likes`);