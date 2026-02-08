# שלב 1: אימג' בסיס קטן (Python 3.9)
FROM python:3.9-slim

# שלב 2: הגדרות סביבה (ברירות מחדל)
ENV PYTHONUNBUFFERED=1
ENV SFTP_PORT=2222
ENV DATA_DIR=/data
ENV SFTP_USER=user1
ENV SFTP_PASS=pass123
ENV ALLOW_DELETE=true

# שלב 3: התקנת ספריית SFTP
RUN pip install --no-cache-dir paramiko

# שלב 4: העתקת קובץ השרת
WORKDIR /app
COPY sftp_server.py .

# שלב 5: הכנת התיקיות
# יצירת תיקיית המידע ותיקיית המפתחות עם הרשאות מלאות
# (כדי שמשתמש אקראי ב-OpenShift יוכל לכתוב אליהן)
RUN mkdir -p /data && chmod 777 /data
RUN mkdir -p /tmp && chmod 777 /tmp

# שלב 6: אבטחה - הרצה כמשתמש רגיל (לא Root)
USER 1000

# שלב 7: הפקודה להרצה
CMD ["python", "sftp_server.py"]