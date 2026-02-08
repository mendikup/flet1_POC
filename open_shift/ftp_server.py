import os
import paramiko
import threading
import socket
import sys
import time
import logging

# הגדרת לוגים ל-STDOUT (כדי שיראו אותם ב-OpenShift Logs)
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
logger = logging.getLogger("sftp-server")

# --- קריאת קונפיגורציה ממשתני סביבה ---
PORT = int(os.getenv("SFTP_PORT", 2222))
DATA_DIR = os.getenv("DATA_DIR", "/data")
USER = os.getenv("SFTP_USER", "user1")
PASS = os.getenv("SFTP_PASS", "pass123")

# דגל האם לאפשר ללקוחות למחוק קבצים (Delete/Rmdir)
# בטסטים נרצה True, בפרודקשן אולי False (כי רק ה-Worker מוחק)
ALLOW_DELETE = os.getenv("ALLOW_DELETE", "true").lower() == "true"

HOST_KEY_PATH = '/tmp/host.key'

# יצירת מפתח שרת אם לא קיים (נוצר ב-/tmp כדי לא לדרוש הרשאות מיוחדות)
if not os.path.exists(HOST_KEY_PATH):
    logger.info("Generating Host Key...")
    key = paramiko.RSAKey.generate(2048)
    key.write_private_key_file(HOST_KEY_PATH)


# --- מחלקה לטיפול בקובץ פתוח ---
class LocalFileHandle(paramiko.SFTPHandle):
    def __init__(self, flags, path, mode):
        super().__init__(flags)
        self._path = path
        self._file = open(path, mode)

    def close(self):
        if not self._file.closed:
            self._file.close()
            logger.info(f"Closed file: {self._path}")
        super().close()

    def read(self, offset, length):
        self._file.seek(offset)
        return self._file.read(length)

    def write(self, offset, data):
        self._file.seek(offset)
        self._file.write(data)
        return paramiko.SFTP_OK

    def stat(self):
        try:
            return paramiko.SFTPAttributes.from_stat(os.fstat(self._file.fileno()))
        except OSError:
            return paramiko.SFTP_FAILURE


# --- הממשק שמקשר בין SFTP למערכת הקבצים ---
class LocalSFTPServerInterface(paramiko.SFTPServerInterface):
    def _resolve(self, path):
        # מנרמל נתיבים כדי שתמיד יהיו תחת DATA_DIR
        if path == '/' or path == '.': return DATA_DIR
        if path.startswith('/'): path = path[1:]
        return os.path.join(DATA_DIR, path)

    def list_folder(self, path):
        path = self._resolve(path)
        try:
            return [paramiko.SFTPAttributes.from_stat(os.stat(os.path.join(path, f)), f) for f in os.listdir(path)]
        except OSError:
            return paramiko.SFTP_FAILURE

    def stat(self, path):
        try:
            return paramiko.SFTPAttributes.from_stat(os.stat(self._resolve(path)))
        except OSError:
            return paramiko.SFTP_NO_SUCH_FILE

    def lstat(self, path):
        return self.stat(path)

    def open(self, path, flags, attr):
        full_path = self._resolve(path)
        logger.info(f"Open request: {path}")
        try:
            # תרגום דגלי SFTP למצבי פתיחה של Python
            mode = 'rb'
            if (flags & os.O_WRONLY) or (flags & os.O_RDWR): mode = 'wb'
            if flags & os.O_APPEND: mode = 'ab'
            return LocalFileHandle(flags, full_path, mode)
        except OSError as e:
            logger.error(f"Failed to open {full_path}: {e}")
            return paramiko.SFTP_FAILURE

    def remove(self, path):
        if not ALLOW_DELETE:
            logger.warning(f"Delete request blocked for: {path}")
            return paramiko.SFTP_PERMISSION_DENIED

        try:
            os.remove(self._resolve(path))
            logger.info(f"Deleted file: {path}")
            return paramiko.SFTP_OK
        except OSError:
            return paramiko.SFTP_FAILURE

    def rename(self, oldpath, newpath):
        try:
            os.rename(self._resolve(oldpath), self._resolve(newpath))
            logger.info(f"Renamed: {oldpath} -> {newpath}")
            return paramiko.SFTP_OK
        except OSError:
            return paramiko.SFTP_FAILURE

    # --- תמיכה בתיקיות ---
    def mkdir(self, path, attr):
        # גם אם התיקיות מגיעות מוכנות, הלקוח (SFTP Client) שולח פקודת mkdir
        # לפני העלאת הקבצים, ולכן חובה לממש את זה.
        try:
            real_path = self._resolve(path)
            os.mkdir(real_path)
            logger.info(f"Created directory: {path}")
            return paramiko.SFTP_OK
        except OSError as e:
            # אם התיקייה כבר קיימת, זה בסדר
            if "File exists" in str(e) or e.errno == 17:
                return paramiko.SFTP_OK
            logger.error(f"Mkdir failed: {e}")
            return paramiko.SFTP_FAILURE

    def rmdir(self, path):
        if not ALLOW_DELETE:
            return paramiko.SFTP_PERMISSION_DENIED

        try:
            os.rmdir(self._resolve(path))
            logger.info(f"Removed directory: {path}")
            return paramiko.SFTP_OK
        except OSError:
            return paramiko.SFTP_FAILURE


# --- ניהול התחברות (Auth) ---
class StubServer(paramiko.ServerInterface):
    def check_channel_request(self, kind, chanid):
        return paramiko.OPEN_SUCCEEDED if kind == 'session' else paramiko.OPEN_FAILED_ADMINISTRATIVELY_PROHIBITED

    def check_auth_password(self, username, password):
        # אימות מול משתני הסביבה
        if username == USER and password == PASS:
            return paramiko.AUTH_SUCCESSFUL
        logger.warning(f"Auth failed for user: {username}")
        return paramiko.AUTH_FAILED

    def get_allowed_auths(self, username):
        return 'password'


def handle_client(conn, addr):
    logger.info(f"New connection from {addr}")
    transport = None
    try:
        transport = paramiko.Transport(conn)
        transport.add_server_key(paramiko.RSAKey(filename=HOST_KEY_PATH))
        transport.set_subsystem_handler('sftp', paramiko.SFTPServer, sftp_si=LocalSFTPServerInterface)
        server = StubServer()
        transport.start_server(server=server)
        channel = transport.accept(20)
        if channel:
            while transport.is_active(): time.sleep(1)
    except Exception as e:
        # שגיאות EOF רגילות כשלקוח מתנתק לא צריכות להציף את הלוג
        if "EOF" not in str(e):
            logger.error(f"Handler error: {e}")
    finally:
        if transport: transport.close()


def start_server():
    # וידוא שתיקיית המידע קיימת
    if not os.path.exists(DATA_DIR):
        try:
            os.makedirs(DATA_DIR)
        except OSError:
            pass  # אולי אין הרשאות ליצור, נניח שהיא קיימת מ-PVC

    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind(('0.0.0.0', PORT))
    s.listen(10)
    logger.info(f"SFTP Server started on port {PORT}")
    logger.info(f"User: {USER}, Allow Delete: {ALLOW_DELETE}")

    while True:
        try:
            conn, addr = s.accept()
            t = threading.Thread(target=handle_client, args=(conn, addr))
            t.daemon = True
            t.start()
        except Exception as e:
            logger.error(f"Accept error: {e}")


if __name__ == "__main__":
    start_server()