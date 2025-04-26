from fastapi import FastAPI, HTTPException, Path
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import sqlite3

app = FastAPI()

# Database setup
def init_db():
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute('''CREATE TABLE IF NOT EXISTS posts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        userName TEXT NOT NULL,
        content TEXT NOT NULL,
        createdAt TEXT NOT NULL,
        updatedAt TEXT NOT NULL,
        likeCount INTEGER NOT NULL,
        commentCount INTEGER NOT NULL
    )''')
    cursor.execute('''CREATE TABLE IF NOT EXISTS comments (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        postId INTEGER NOT NULL,
        userName TEXT NOT NULL,
        content TEXT NOT NULL,
        createdAt TEXT NOT NULL,
        updatedAt TEXT NOT NULL,
        FOREIGN KEY(postId) REFERENCES posts(id)
    )''')
    conn.commit()
    conn.close()

init_db()

# Pydantic Models
class Post(BaseModel):
    id: int
    userName: str
    content: str
    createdAt: datetime
    updatedAt: datetime
    likeCount: int
    commentCount: int

class CreatePostRequest(BaseModel):
    userName: str
    content: str

class UpdatePostRequest(BaseModel):
    content: str

class Comment(BaseModel):
    id: int
    postId: int
    userName: str
    content: str
    createdAt: datetime
    updatedAt: datetime

class CreateCommentRequest(BaseModel):
    userName: str
    content: str

class UpdateCommentRequest(BaseModel):
    content: str

class LikeRequest(BaseModel):
    userName: str

class ErrorResponse(BaseModel):
    message: str

# Routes
@app.get("/api/posts", response_model=List[Post])
def get_posts():
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts")
    rows = cursor.fetchall()
    conn.close()
    return [Post(id=row[0], userName=row[1], content=row[2], createdAt=row[3], updatedAt=row[4], likeCount=row[5], commentCount=row[6]) for row in rows]

@app.post("/api/posts", response_model=Post, status_code=201)
def create_post(request: CreatePostRequest):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    cursor.execute("INSERT INTO posts (userName, content, createdAt, updatedAt, likeCount, commentCount) VALUES (?, ?, ?, ?, 0, 0)", (request.userName, request.content, now, now))
    post_id = cursor.lastrowid
    conn.commit()
    conn.close()
    return Post(id=post_id, userName=request.userName, content=request.content, createdAt=now, updatedAt=now, likeCount=0, commentCount=0)

@app.get("/api/posts/{postId}", response_model=Post)
def get_post(postId: int = Path(..., description="조회하려는 포스트의 ID")):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM posts WHERE id = ?", (postId,))
    row = cursor.fetchone()
    conn.close()
    if row:
        return Post(id=row[0], userName=row[1], content=row[2], createdAt=row[3], updatedAt=row[4], likeCount=row[5], commentCount=row[6])
    raise HTTPException(status_code=404, detail="포스트를 찾을 수 없음")

@app.patch("/api/posts/{postId}", response_model=Post)
def update_post(postId: int, request: UpdatePostRequest):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    cursor.execute("UPDATE posts SET content = ?, updatedAt = ? WHERE id = ?", (request.content, now, postId))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="포스트를 찾을 수 없음")
    conn.commit()
    cursor.execute("SELECT * FROM posts WHERE id = ?", (postId,))
    row = cursor.fetchone()
    conn.close()
    return Post(id=row[0], userName=row[1], content=row[2], createdAt=row[3], updatedAt=row[4], likeCount=row[5], commentCount=row[6])

@app.delete("/api/posts/{postId}", status_code=204)
def delete_post(postId: int):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM posts WHERE id = ?", (postId,))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="포스트를 찾을 수 없음")
    conn.commit()
    conn.close()
    return

@app.get("/api/posts/{postId}/comments", response_model=List[Comment])
def get_comments(postId: int):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM comments WHERE postId = ?", (postId,))
    rows = cursor.fetchall()
    conn.close()
    return [Comment(id=row[0], postId=row[1], userName=row[2], content=row[3], createdAt=row[4], updatedAt=row[5]) for row in rows]

@app.post("/api/posts/{postId}/comments", response_model=Comment, status_code=201)
def create_comment(postId: int, request: CreateCommentRequest):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    cursor.execute("INSERT INTO comments (postId, userName, content, createdAt, updatedAt) VALUES (?, ?, ?, ?, ?)", (postId, request.userName, request.content, now, now))
    comment_id = cursor.lastrowid
    cursor.execute("UPDATE posts SET commentCount = commentCount + 1 WHERE id = ?", (postId,))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="포스트를 찾을 수 없음")
    conn.commit()
    conn.close()
    return Comment(id=comment_id, postId=postId, userName=request.userName, content=request.content, createdAt=now, updatedAt=now)

@app.get("/api/posts/{postId}/comments/{commentId}", response_model=Comment)
def get_comment(postId: int, commentId: int):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM comments WHERE postId = ? AND id = ?", (postId, commentId))
    row = cursor.fetchone()
    conn.close()
    if row:
        return Comment(id=row[0], postId=row[1], userName=row[2], content=row[3], createdAt=row[4], updatedAt=row[5])
    raise HTTPException(status_code=404, detail="댓글 또는 포스트를 찾을 수 없음")

@app.patch("/api/posts/{postId}/comments/{commentId}", response_model=Comment)
def update_comment(postId: int, commentId: int, request: UpdateCommentRequest):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    now = datetime.now().isoformat()
    cursor.execute("UPDATE comments SET content = ?, updatedAt = ? WHERE postId = ? AND id = ?", (request.content, now, postId, commentId))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="댓글 또는 포스트를 찾을 수 없음")
    conn.commit()
    cursor.execute("SELECT * FROM comments WHERE postId = ? AND id = ?", (postId, commentId))
    row = cursor.fetchone()
    conn.close()
    return Comment(id=row[0], postId=row[1], userName=row[2], content=row[3], createdAt=row[4], updatedAt=row[5])

@app.delete("/api/posts/{postId}/comments/{commentId}", status_code=204)
def delete_comment(postId: int, commentId: int):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute("DELETE FROM comments WHERE postId = ? AND id = ?", (postId, commentId))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="댓글 또는 포스트를 찾을 수 없음")
    cursor.execute("UPDATE posts SET commentCount = commentCount - 1 WHERE id = ?", (postId,))
    conn.commit()
    conn.close()
    return

@app.post("/api/posts/{postId}/likes", status_code=201)
def like_post(postId: int, request: LikeRequest):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE posts SET likeCount = likeCount + 1 WHERE id = ?", (postId,))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="포스트를 찾을 수 없음")
    conn.commit()
    conn.close()
    return

@app.delete("/api/posts/{postId}/likes", status_code=204)
def unlike_post(postId: int):
    conn = sqlite3.connect("app.db")
    cursor = conn.cursor()
    cursor.execute("UPDATE posts SET likeCount = likeCount - 1 WHERE id = ? AND likeCount > 0", (postId,))
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="포스트를 찾을 수 없음")
    conn.commit()
    conn.close()
    return