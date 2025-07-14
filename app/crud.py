from .database import get_db_connection


def get_top_products(limit: int = 10):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        SELECT product_name, COUNT(*) AS mention_count
        FROM analytics.fct_messages
        WHERE product_name IS NOT NULL
        GROUP BY product_name
        ORDER BY mention_count DESC
        LIMIT %s;
    """
    cursor.execute(query, (limit,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results


def get_channel_activity(channel_name: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        SELECT channel_name, date_trunc('day', date_posted) AS day, COUNT(*) 
        AS daily_post_count
        FROM analytics.fct_messages
        WHERE channel_name = %s
        GROUP BY channel_name, day
        ORDER BY day DESC
        LIMIT 30;
    """
    cursor.execute(query, (channel_name,))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results


def search_messages(query_text: str):
    conn = get_db_connection()
    cursor = conn.cursor()
    query = """
        SELECT message_id, channel_name, message_text, date_posted
        FROM analytics.fct_messages
        WHERE message_text ILIKE %s
        ORDER BY date_posted DESC
        LIMIT 50;
    """
    cursor.execute(query, (f"%{query_text}%",))
    results = cursor.fetchall()
    cursor.close()
    conn.close()
    return results
