# -*- coding: utf-8 -*-
import json

with open(r"c:\ReadAWrite\data\real_editor_fields.json", encoding="utf-8") as f:
    fields = json.load(f)

for f in fields:
    if f.get("id") or f.get("name") or f.get("placeholder"):
        print(f"[{f['tag']}] id='{f['id']}' name='{f['name']}' type='{f['type']}' placeholder='{f['placeholder']}'")
