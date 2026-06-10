#!/usr/bin/env python3
"""Parse Glitchtip event JSON from stdin and print structured error data."""
import json
import sys

data = json.load(sys.stdin)
for ev in data:
    for entry in ev.get("entries", []):
        if entry.get("type") == "exception":
            for val in entry["data"].get("values", []):
                print("Type:", val.get("type"))
                print("Value:", val.get("value"))
                for f in val.get("stacktrace", {}).get("frames") or []:
                    print(
                        f'  {f.get("filename", "?")}:{f.get("lineNo", "?")}'
                        f' in {f.get("function", "?")}'
                    )
        elif entry.get("type") == "message":
            print("Message:", entry.get("data", {}).get("formatted", ""))
