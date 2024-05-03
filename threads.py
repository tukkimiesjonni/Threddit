import os
from hashlib import sha256
from db import db
from flask import session, abort, request
from werkzeug.security import check_password_hash, generate_password_hash
from sqlalchemy.sql import text
from datetime import datetime
from users import get_user_id


def get_timestamp():
    time = datetime.now()
    return time


def create_thread(title, content):

    user_id = get_user_id()
    time = get_timestamp()

    query = text("""
        INSERT INTO threads (user_id, title, content, published)
        VALUES (:user_id, :title, :content, :published)
    """)

    db.session.execute(query, {"user_id":user_id, "title":title, "content":content, "published":time})
    db.session.commit()
    print("thread added")
    return True


def get_thread_id(thread):
    query = text("""
        SELECT id FROM threads
        WHERE title = (:title)
    """)

    query_result = db.session.execute(query, {"title":thread})
    thread_id = query_result.fetchone()[0]

    return thread_id


def add_comment(thread, comment):

    time = get_timestamp()
    thread_id = get_thread_id(thread)
    user_id = get_user_id(session["username"])


    query = text("""
        INSERT INTO comments (user_id, thread_id, comment, published)
        VALUES (:user_id, :thread_id, :comment, :time)
    """)

    db.session.execute(query, {"user_id":user_id, "thread_id":thread_id, "comment":comment, "time":time})
    db.session.commit()


def get_threads():
    query = text("""
        SELECT threads.id, name, title, content, published
        FROM users
        JOIN threads 
        ON users.id = threads.user_id
    """)

    query_result = db.session.execute(query)
    result = query_result.fetchall()

    return result


def get_thread(thread_id):
    query = text("""
        SELECT name, title, content, published
        FROM users
        JOIN threads
        ON users.id = threads.user_id
        WHERE threads.id = (:thread_id)
    """)

    query_result = db.session.execute(query, {"thread_id":thread_id})
    result = query_result.fetchone()

    return result


def upvote(thread_id):
    query = text("""
    INSERT INTO votes (thread_id, vote)
    VALUES (:thread_id, 1)
    """)

    db.session.execute(query, {"thread_id":thread_id})
    db.session.commit()


def downvote(thread_id):
    query = text("""
    INSERT INTO votes (thread_id, vote)
    VALUES (:thread_id, 0)
    """)

    db.session.execute(query, {"thread_id":thread_id})
    db.session.commit()


def count_votes(thread_id):
    query = text("""
        COUNT(*) FROM votes
        WHERE thread_id = (:thread_id)
    """)

    query_result = db.session.execute(query, {"thread_id":thread_id})
    result = query_result.fetchone()

    return result


def new_comment(thread_id, user_id, comment):
    query = text("""
        INSERT INTO comments (thread_id, user_id, comment)
        VALUES (:thread_id, :user_id, :comment)
    """)

    db.session.execute(query, {"thread_id":thread_id, "user_id":user_id, "comment":comment})
    db.session.commit()


def get_comments(thread_id):
    query = text("""
        SELECT * FROM comments
        WHERE thread_id = (:thread_id)
    """)

    query_result = db.session.execute(query, {"thread_id":thread_id})
    result = query_result.fetchall()

    return result