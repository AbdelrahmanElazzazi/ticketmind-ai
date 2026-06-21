import sqlite3

DB_NAME = "review_queue.db"

# Initialize Database & Create Table
#-------------------------
def initialize_database():
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute("""
    CREATE TABLE IF NOT EXISTS review_queue (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    ticket_id INTEGER,
    request_id TEXT,
    question TEXT,
    answer TEXT,
    context TEXT,
    score REAL,
    status TEXT,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    )
    """)
    
    conn.commit()
    conn.close()

# Get Review For Approval
#------------------------------
def get_review_for_approval(review_id):

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM review_queue
        WHERE id = ?
        """,
        (review_id,)
    )

    row = cursor.fetchone()

    conn.close()

    if not row:
        return None

    return {
        "id": row["id"],
        "ticket_id": row["ticket_id"],
        "answer": row["answer"]
    }

# Add A Ticket To Review Queue
#---------------------------
def add_to_review_queue(ticket_id, request_id, question, answer, score, context):
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute(
        """
        INSERT INTO review_queue
        (
            ticket_id,
            request_id,
            question,
            answer,
            context,
            score,
            status
        )
        VALUES (?, ?, ?, ?, ?, ?, ?)
        """,
        (
            ticket_id,
            request_id,
            question,
            answer,
            context,
            score,
            "PENDING"
        )
    )

    conn.commit()
    conn.close()

# Get All Pending Tickets For Review
#------------------------
def get_pending_reviews():

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row
    cursor = conn.cursor()

    cursor.execute("""
    SELECT *
    FROM review_queue
    WHERE status = 'PENDING'
    ORDER BY created_at DESC
    """)

    rows = cursor.fetchall()
    reviews = []

    for row in rows:
        reviews.append(
            {
                "id": row["id"],
                "ticket_id": row["ticket_id"],
                "request_id": row["request_id"],
                "question": row["question"],
                "answer": row["answer"],
                "context": row["context"],
                "score": row["score"],
                "status": row["status"],
                "created_at": row["created_at"]
            }
        )
    conn.close()
    return reviews

# Check Spacific Answer By ID
#--------------------------------
def get_review_by_id(review_id):

    conn = sqlite3.connect(DB_NAME)
    conn.row_factory = sqlite3.Row

    cursor = conn.cursor()

    cursor.execute(
        """
        SELECT *
        FROM review_queue
        WHERE id = ?
        """,
        (review_id,)
    )

    row = cursor.fetchone()
    conn.close()

    if not row:
        return None

    return {
        "id": row["id"],
        "ticket_id": row["ticket_id"],
        "request_id": row["request_id"],
        "question": row["question"],
        "answer": row["answer"],
        "context": row["context"],
        "score": row["score"],
        "status": row["status"],
        "created_at": row["created_at"]
    }

# Approve An Answer
#----------------
def approve_review(review_id):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE review_queue
        SET status = 'APPROVED'
        WHERE id = ?
        """,
        (review_id,)
    )

    conn.commit()
    conn.close()

# Reject Answer
#---------------
def reject_review(review_id):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE review_queue
        SET status = 'REJECTED'
        WHERE id = ?
        """,
        (review_id,)
    )

    conn.commit()
    conn.close()

# Update & Approve Answer
#--------------------
def update_review_answer(review_id, answer):

    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()

    cursor.execute(
        """
        UPDATE review_queue
        SET answer = ?
        WHERE id = ?
        """,
        (
            answer,
            review_id
        )
    )

    conn.commit()
    conn.close()