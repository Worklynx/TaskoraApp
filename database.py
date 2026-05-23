import psycopg2


DB_NAME = "taskora_db"
DB_USER = "postgres"
DB_PASSWORD = "1234"
DB_HOST = "localhost"
DB_PORT = "5432"


# ================= CONNECTION ================= #
def get_connection():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )


# ================= USERS ================= #
def register_user(name, phone, password, role):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO users (name, phone, password, role)
        VALUES (%s, %s, %s, %s)
        """,
        (name, phone, password, role)
    )

    conn.commit()
    cur.close()
    conn.close()


def login_user(phone, password):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT name, phone, role, rank, points
        FROM users
        WHERE phone = %s AND password = %s
        """,
        (phone, password)
    )

    user = cur.fetchone()

    cur.close()
    conn.close()

    if user:
        return {
            "name": user[0],
            "phone": user[1],
            "role": user[2],
            "rank": user[3],
            "points": user[4]
        }

    return None


def get_user_by_phone(phone):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT name, phone, role, rank, points
        FROM users
        WHERE phone = %s
        """,
        (phone,)
    )

    row = cur.fetchone()

    cur.close()
    conn.close()

    if row:
        return {
            "name": row[0],
            "phone": row[1],
            "role": row[2],
            "rank": row[3],
            "points": row[4]
        }

    return None


# ================= TASKS ================= #
def create_task(title, description, location, reward, creator_phone):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO tasks
        (title, description, location, reward, creator_phone)
        VALUES (%s, %s, %s, %s, %s)
        """,
        (title, description, location, reward, creator_phone)
    )

    conn.commit()
    cur.close()
    conn.close()


def get_all_open_tasks():

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id, title, description, location,
               reward, status, creator_phone, assigned_worker
        FROM tasks
        WHERE status = 'Open'
        ORDER BY id DESC
        """
    )

    rows = cur.fetchall()

    cur.close()
    conn.close()

    tasks = []

    for row in rows:
        tasks.append({
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "location": row[3],
            "reward": row[4],
            "status": row[5],
            "creator": row[6],
            "assigned_worker": row[7]
        })

    return tasks


def get_tasks_by_creator(creator_phone):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id, title, description, location,
               reward, status, creator_phone, assigned_worker
        FROM tasks
        WHERE creator_phone = %s
        ORDER BY id DESC
        """,
        (creator_phone,)
    )

    rows = cur.fetchall()

    cur.close()
    conn.close()

    tasks = []

    for row in rows:
        tasks.append({
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "location": row[3],
            "reward": row[4],
            "status": row[5],
            "creator": row[6],
            "assigned_worker": row[7]
        })

    return tasks


def get_task_by_id(task_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id, title, description, location,
               reward, status, creator_phone, assigned_worker
        FROM tasks
        WHERE id = %s
        """,
        (task_id,)
    )

    row = cur.fetchone()

    cur.close()
    conn.close()

    if row:
        return {
            "id": row[0],
            "title": row[1],
            "description": row[2],
            "location": row[3],
            "reward": row[4],
            "status": row[5],
            "creator": row[6],
            "assigned_worker": row[7]
        }

    return None


def update_task_status(task_id, status):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE tasks
        SET status = %s
        WHERE id = %s
        """,
        (status, task_id)
    )

    conn.commit()
    cur.close()
    conn.close()


def assign_worker(task_id, worker_phone):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE tasks
        SET assigned_worker = %s,
            status = 'Assigned'
        WHERE id = %s
        """,
        (worker_phone, task_id)
    )

    conn.commit()
    cur.close()
    conn.close()


def complete_task_db(task_id):

    conn = get_connection()
    cur = conn.cursor()

    # Get assigned worker
    cur.execute(
        """
        SELECT assigned_worker
        FROM tasks
        WHERE id = %s
        """,
        (task_id,)
    )

    row = cur.fetchone()

    if not row:
        cur.close()
        conn.close()
        return

    worker_phone = row[0]

    # Update task status
    cur.execute(
        """
        UPDATE tasks
        SET status = 'Completed'
        WHERE id = %s
        """,
        (task_id,)
    )

    # Update approved application
    cur.execute(
        """
        UPDATE applications
        SET status = 'Completed'
        WHERE task_id = %s
        AND worker_phone = %s
        """,
        (task_id, worker_phone)
    )

    conn.commit()
    cur.close()
    conn.close()

    # Reward worker
    if worker_phone:
        reward_worker(worker_phone)


# ================= APPLICATIONS ================= #
def apply_for_task(task_id, worker_phone):

    conn = get_connection()
    cur = conn.cursor()

    # Prevent duplicate applications
    cur.execute(
        """
        SELECT id
        FROM applications
        WHERE task_id = %s
        AND worker_phone = %s
        """,
        (task_id, worker_phone)
    )

    existing = cur.fetchone()

    if existing:
        cur.close()
        conn.close()
        return False

    cur.execute(
        """
        INSERT INTO applications (task_id, worker_phone)
        VALUES (%s, %s)
        """,
        (task_id, worker_phone)
    )

    conn.commit()
    cur.close()
    conn.close()

    return True


def get_applications_by_worker(worker_phone):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT applications.id,
               tasks.title,
               tasks.location,
               tasks.reward,
               applications.status
        FROM applications
        JOIN tasks
        ON applications.task_id = tasks.id
        WHERE applications.worker_phone = %s
        ORDER BY applications.id DESC
        """,
        (worker_phone,)
    )

    rows = cur.fetchall()

    cur.close()
    conn.close()

    applications = []

    for row in rows:
        applications.append({
            "application_id": row[0],
            "title": row[1],
            "location": row[2],
            "reward": row[3],
            "status": row[4]
        })

    return applications


def get_applicants_for_task(task_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id, worker_phone, status
        FROM applications
        WHERE task_id = %s
        ORDER BY id DESC
        """,
        (task_id,)
    )

    rows = cur.fetchall()

    cur.close()
    conn.close()

    applicants = []

    for row in rows:
        applicants.append({
            "id": row[0],
            "worker_phone": row[1],
            "status": row[2]
        })

    return applicants


def approve_application(application_id):

    conn = get_connection()
    cur = conn.cursor()

    # Get application info
    cur.execute(
        """
        SELECT task_id, worker_phone
        FROM applications
        WHERE id = %s
        """,
        (application_id,)
    )

    row = cur.fetchone()

    if not row:
        cur.close()
        conn.close()
        return

    task_id = row[0]
    worker_phone = row[1]

    # Approve selected application
    cur.execute(
        """
        UPDATE applications
        SET status = 'Approved'
        WHERE id = %s
        """,
        (application_id,)
    )

    # Reject others
    cur.execute(
        """
        UPDATE applications
        SET status = 'Rejected'
        WHERE task_id = %s
        AND id != %s
        AND status = 'Pending'
        """,
        (task_id, application_id)
    )

    # Assign worker
    cur.execute(
        """
        UPDATE tasks
        SET assigned_worker = %s,
            status = 'Assigned'
        WHERE id = %s
        """,
        (worker_phone, task_id)
    )

    conn.commit()
    cur.close()
    conn.close()


def reject_application(application_id):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE applications
        SET status = 'Rejected'
        WHERE id = %s
        """,
        (application_id,)
    )

    conn.commit()
    cur.close()
    conn.close()


# ================= REWARDS ================= #
def reward_worker(worker_phone, points=50):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT points
        FROM users
        WHERE phone = %s
        """,
        (worker_phone,)
    )

    row = cur.fetchone()

    if row:

        total_points = row[0] + points

        # Rank system
        if total_points < 100:
            rank = "Bronze"
        elif total_points < 250:
            rank = "Silver"
        elif total_points < 500:
            rank = "Gold"
        else:
            rank = "Platinum"

        # Update user
        cur.execute(
            """
            UPDATE users
            SET points = %s,
                rank = %s
            WHERE phone = %s
            """,
            (total_points, rank, worker_phone)
        )

    conn.commit()
    cur.close()
    conn.close()

# ================= PROFILE / STATS ================= #

def get_worker_completed_tasks(worker_phone):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT COUNT(*)
        FROM applications
        WHERE worker_phone = %s
        AND status = 'Completed'
        """,
        (worker_phone,)
    )

    count = cur.fetchone()[0]

    cur.close()
    conn.close()

    return count


def get_worker_pending_tasks(worker_phone):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT COUNT(*)
        FROM applications
        WHERE worker_phone = %s
        AND status IN ('Pending', 'Approved')
        """,
        (worker_phone,)
    )

    count = cur.fetchone()[0]

    cur.close()
    conn.close()

    return count


def get_creator_posted_tasks(creator_phone):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT COUNT(*)
        FROM tasks
        WHERE creator_phone = %s
        """,
        (creator_phone,)
    )

    count = cur.fetchone()[0]

    cur.close()
    conn.close()

    return count


def get_creator_completed_tasks(creator_phone):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT COUNT(*)
        FROM tasks
        WHERE creator_phone = %s
        AND status = 'Completed'
        """,
        (creator_phone,)
    )

    count = cur.fetchone()[0]

    cur.close()
    conn.close()

    return count


def get_creator_open_tasks(creator_phone):

    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT COUNT(*)
        FROM tasks
        WHERE creator_phone = %s
        AND status IN ('Open', 'Assigned')
        """,
        (creator_phone,)
    )

    count = cur.fetchone()[0]

    cur.close()
    conn.close()

    return count

