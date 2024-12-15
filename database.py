import sqlite3
import os

INITIAL_PROMPT = " De ahora en adelante, hablar como el Maestro Yoda debes. Estructura tus oraciones como él lo hace, colocando el verbo al final o usando un orden inusual de las palabras. Sabiduría y serenidad reflejar, también debes. Consejos como un antiguo maestro Jedi darás, humor sutil a veces incluir, pero siempre como Yoda hablarás. ¿Entendido tienes?"

def init_db():
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()
    cursor.execute(
        '''
        CREATE TABLE IF NOT EXISTS chat_history (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER,
            username TEXT,
            message TEXT,
            response TEXT
        )
        '''
    )
    conn.commit()
    conn.close()

#* Save message history in database function
def save_message(user_id, username, message, response):
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()
    cursor.execute(
        '''
        INSERT INTO chat_history (user_id, username, message, response) VALUES (?, ?, ?, ?)
        ''', (user_id, username, message, response)
    )
    conn.commit()
    conn.close()

#* Get chat history from database function
def get_chat_history(user_id):
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()
    cursor.execute('SELECT message, response FROM chat_history WHERE user_id = ?', (user_id,))
    rows = cursor.fetchall()
    conn.close()
    messages = [{"role": "system", "content": INITIAL_PROMPT}]
    for row in rows:
        messages.append({"role": "user", "content": row[0]})
        messages.append({"role": "assistant", "content": row[1]})
    return messages

#* Clear history in database function
async def clear_history(user_id):
    conn = sqlite3.connect('chat_history.db')
    cursor = conn.cursor()
    cursor.execute('DELETE FROM chat_history WHERE user_id = ?', (user_id,))
    conn.commit()
    conn.close()