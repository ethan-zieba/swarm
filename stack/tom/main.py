import time
import requests
import yaml


def load_config(path="tom_config.yml"):
    try:
        with open(path, 'r') as f:
            return yaml.safe_load(f)
    except Exception as e:
        print(f"Failed to load config from {path}: {e}")
        return {}

config = load_config()

NADIR_ENDPOINT = config.get("nadir_endpoint", "http://192.168.121.1:3100/nadir/api/v1/push")
HOSTNAME = config.get("hostname", "walid")
LOG_FILE = config.get("log_file", "/var/log/testlogs.log")

MEASUREMENT_TYPE = ["logs", "metric"]
TAGS = {"job": "tom_agent", "host": "walid"}

def log_tailing(file):
    file.seek(0, 2)
    while True:
        line = file.readline()
        if not line:
            time.sleep(0.2)
            continue
        yield line

def format_log(tags, fields, measurement="logs", timestamp=None):
    tags_string = ",".join([f"{tag}={value}" for tag, value in tags.items()])

    escaped_fields = {key: str(value).replace("\\", "\\\\").replace('"', '\\"') for key, value in fields.items()}

    field_string = ",".join([
    f'{key}="{escaped_value}"' for key, escaped_value in escaped_fields.items()
    ])

    if timestamp is None:
        timestamp = int(time.time() * 1e9)  # nanoseconds
    return f"{measurement},{tags_string} {field_string} {timestamp}"

def push_log_to_nadir(line, source):
    cleaned_line = line.strip().replace('\u00a0', ' ')
    #cleaned_line = line.strip()
    new_tags = TAGS.copy()
    new_tags["source"] = source

    payload = format_log(measurement=MEASUREMENT_TYPE[0], tags=new_tags, fields={"message": cleaned_line})
    print(f"Sending log {payload} to {NADIR_ENDPOINT}")
    try:
        response = requests.post(NADIR_ENDPOINT, data=payload)
        if response.status_code != 204:
            print("Failed to send log:", response.text)
    except Exception as e:
        print("Error:", e)

def main():
    push_log_to_nadir(f"Starting T.O.M on {TAGS['host']}", source="TOM")
    with open(LOG_FILE, "r") as logfile:
        for line in log_tailing(logfile):
            push_log_to_nadir(line, source=LOG_FILE) # Here for this testing version

if __name__ == "__main__":
    main()
