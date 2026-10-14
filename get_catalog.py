"""Turn a Drive download_file_content result (sheet exported as text/csv, base64) into catalog.csv.
Usage: python3 get_catalog.py RESULT_FILE"""
import base64, json, os, sys
j = json.load(open(sys.argv[1]))
c = j["content"]
try:
    data = base64.b64decode(c, validate=True).decode("utf-8")
except Exception:
    data = c
open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "catalog.csv"), "w", encoding="utf-8").write(data)
print("catalog.csv rows:", data.count("\n"), "| header:", data.split("\n", 1)[0][:120])
