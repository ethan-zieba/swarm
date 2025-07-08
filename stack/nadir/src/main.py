from http.server import HTTPServer, BaseHTTPRequestHandler
from influxdb import InfluxDBClient
import json

def read_secret(path):
    try:
        with open(path, 'r') as f:
            return f.read().strip()
    except Exception as e:
        print(f"[N.A.D.I.R] Failed to read secret from {path}: {e}")
        return None

INFLUX_DB_NAME = read_secret("/run/secrets/influxdb_name")
INFLUX_DB_USER = read_secret("/run/secrets/influxdb_user")
INFLUX_DB_PASSWORD = read_secret("/run/secrets/influxdb_password")

client = InfluxDBClient(host='influxdb', port=8086, username=INFLUX_DB_USER, password=INFLUX_DB_PASSWORD)
client.switch_database(INFLUX_DB_NAME)

class NadirHandler(BaseHTTPRequestHandler):
    def do_POST(self):
        if self.path != "/nadir/api/v1/push":
            self.send_response(404)
            self.end_headers()
            self.wfile.write(b"Endpoint not found")
            return

        content_length = int(self.headers.get('Content-Length', 0))
        raw_data = self.rfile.read(content_length)

        try:
            payload = raw_data.decode('utf-8').strip()
            lines = payload.strip().split("\n")
            points = []
            for line in lines:
                try:
                    point = parse_received_log(line)
                    points.append(point)
                except Exception as e:
                    print("Skipping malformed line:", line)
                    print("Error:", e)

            if points:
                client.write_points(points, time_precision='n')
            self.send_response(204)
            self.end_headers()

        except Exception as e:
            self.send_response(500)
            self.end_headers()
            error_msg = f"[N.A.D.I.R] Error decoding log: {e}"
            print(error_msg)
            self.wfile.write(error_msg.encode())

def load_touchy_commands(path="touchy.yml"):
    try:
        with open(path, "r") as f:
            config = yaml.safe_load(f)
            commands = config.get("touchy_commands", [])
            return [(item['command'], item['level'], item['title']) for item in commands]
    except Exception as e:
        print(f"[N.A.D.I.R] Failed to load touchy commands file '{path}': {e}")
        return [("rm -rf", 5), ("sudo", 4)]

def analyse_message(message):
    alert_level = 0
    alert_title = "Info"
    touchy_commands = load_touchy_commands()
    print(f"[N.A.D.I.R] Touchy commands from config: {touchy_commands}")
    for command in touchy_commands:
        if command[0] in message:
            alert_level = command[1]
            alert_title = command.get('title', 'Info')
            break
    return [f"alert_level={alert_level}", f"alert={alert_title}"]

def parse_received_log(line):
    #Log is in the format: logs,job=tom_agent,host=host,source=src message="msg" timestamp
    base_line, timestamp = line.rsplit(" ", 1)
    measurement_part, field_part = base_line.split(" ", 1)

    # So here we have: measurement_part, field_part, timestamp

    measurement_tags = measurement_part.split(",")
    # Now we have: ["logs","job=tom_agent","host=host","source=src"]

    measurement = measurement_tags[0]
    tags = measurement_tags[1:]
    alert_tags = analyse_message(field_part)

    tags = alert_tags + tags
    tags = dict(tag.split("=") for tag in tags)

    fields = dict()
    for field in field_part.split(","):
        k, v = field.split("=")
        fields[k] = v.strip('"')
    point = {
        "measurement": measurement,
        "tags": tags,
        "fields": fields,
        "time": int(timestamp)
    }
    return point

def run_server(port=3100):
    print(f"N.A.D.I.R listening on port {port}...")
    server_address = ('0.0.0.0', port)
    httpd = HTTPServer(server_address, NadirHandler)
    httpd.serve_forever()

if __name__ == "__main__":
    run_server()
