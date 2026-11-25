"""Local-only UI and API backed by a process-local mock table, never AWS."""
import json
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from pathlib import Path
from threading import Lock

from Backend.GETmethod import get_students
from Backend.POSTmethod import add_student


class LocalTable:
    def __init__(self):
        self.items = []
        self.lock = Lock()

    def scan(self, **kwargs):
        with self.lock:
            return {"Items": list(self.items)}

    def put_item(self, Item):
        with self.lock:
            self.items.append(Item)


TABLE = LocalTable()


class Handler(SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(Path(__file__).parent / "Frontend"), **kwargs)

    def reply(self, status, data):
        content = json.dumps(data).encode()
        self.send_response(status)
        self.send_header("Content-Type", "application/json")
        self.send_header("Content-Length", str(len(content)))
        self.end_headers()
        self.wfile.write(content)

    def do_GET(self):
        if self.path == "/api/getStudent":
            return self.reply(200, get_students(TABLE))
        return super().do_GET()

    def do_POST(self):
        if self.path != "/api/addStudent":
            return self.reply(404, {"error": "Not found"})
        try:
            length = int(self.headers.get("Content-Length", "0"))
            if not 0 < length <= 8192:
                raise ValueError("Invalid length")
            event = json.loads(self.rfile.read(length))
        except (ValueError, TypeError):
            return self.reply(400, {"error": "Invalid JSON"})
        result = add_student(event, TABLE)
        self.reply(result["statusCode"], result)


if __name__ == "__main__":
    print("Local student registry: http://127.0.0.1:8080 (in-memory data only)")
    ThreadingHTTPServer(("127.0.0.1", 8080), Handler).serve_forever()
