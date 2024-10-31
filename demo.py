import http.server
import socketserver
import requests
import json
import sqlite3
import os

feishu_webhook_url = 'https://open.feishu.cn/open-apis/bot/v2/hook/xxxxxxxxxxxxxxxxxxx'
DATABASE_NAME = 'request_logs.db'

def initialize_database():
    if not os.path.exists(DATABASE_NAME):
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute('''
            CREATE TABLE requests (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                visitor_ip TEXT NOT NULL,
                accessed_url TEXT NOT NULL
            )
        ''')
        conn.commit()
        conn.close()

class RequestHandler(http.server.SimpleHTTPRequestHandler):

    def do_GET(self):
        visitor_ip = self.client_address[0]
        accessed_url = f'http://{self.headers["Host"]}{self.path}'

        self.log_request_to_db(visitor_ip, accessed_url)

        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write(b"Hello World")

        self.send_feishu_message(visitor_ip, accessed_url)

    def log_request_to_db(self, ip, url):
        conn = sqlite3.connect(DATABASE_NAME)
        cursor = conn.cursor()
        cursor.execute('INSERT INTO requests (visitor_ip, accessed_url) VALUES (?, ?)', (ip, url))
        conn.commit()
        conn.close()

    def send_feishu_message(self, ip, url):
        message_data = {
            "msg_type": "text",
            "content": {
                "text": f"访问者IP: {ip}\n访问的URL: {url}"
            }
        }

        headers = {'Content-Type': 'application/json'}
        response = requests.post(feishu_webhook_url, headers=headers, data=json.dumps(message_data))

        if response.status_code == 200:
            print("消息发送成功！")
        else:
            print(f"消息发送失败：{response.status_code} - {response.text}")

initialize_database()

PORT = 8888
with socketserver.TCPServer(("", PORT), RequestHandler) as httpd:
    print(f"Serving on port {PORT}")
    httpd.serve_forever()
