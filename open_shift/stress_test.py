import paramiko
import time
import os
import random

# הגדרות חיבור
HOST = 'localhost'
PORT = 2222
USER = 'user1'
PASS = 'pass123'

# כמה קבצים לשלוח?
FILE_COUNT = 50


def run_load_test():
    print(f"--- Starting Load Test: Sending {FILE_COUNT} files to SFTP ---")

    try:
        # 1. התחברות לשרת
        print(f"Connecting to {HOST}:{PORT}...")
        transport = paramiko.Transport((HOST, PORT))
        transport.connect(username=USER, password=PASS)
        sftp = paramiko.SFTPClient.from_transport(transport)
        print("Connected successfully!")

        start_time = time.time()

        # 2. לולאת שליחה
        for i in range(1, FILE_COUNT + 1):
            # יצירת שם קובץ ותוכן ייחודיים
            filename = f"bulk_test_file_{i}.txt"
            remote_path = f"/data/{filename}"
            content = f"This is file number {i}.\nRandom data: {random.randint(1000, 9999)}\nTimestamp: {time.time()}"

            # יצירת הקובץ מקומית (זמני)
            with open(filename, "w") as f:
                f.write(content)

            # העלאה
            print(f"[{i}/{FILE_COUNT}] Uploading {filename}...", end='\r')
            sftp.put(filename, remote_path)

            # ניקוי מקומי
            os.remove(filename)

            # השהייה קטנה כדי לא להקריס את ה-Socket המקומי (אופציונלי)
            time.sleep(0.1)

        total_time = time.time() - start_time
        print(f"\n\n--- Finished! ---")
        print(f"Sent {FILE_COUNT} files in {total_time:.2f} seconds.")
        print(f"Average speed: {FILE_COUNT / total_time:.2f} files/sec")

        sftp.close()
        transport.close()

    except Exception as e:
        print(f"\nError: {e}")
        print("Tip: Make sure 'oc port-forward' is running!")


if __name__ == "__main__":
    run_load_test()