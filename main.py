
import json
import gzip
import xml.etree.ElementTree as ET
from pathlib import Path

BASE = Path(__file__).parent
OUTPUT = BASE / "output"
OUTPUT.mkdir(exist_ok=True)

with open(BASE / "channels.json", encoding="utf-8") as f:
    channels = json.load(f)

with open(BASE / "schedule.json", encoding="utf-8") as f:
    schedule = json.load(f)

root = ET.Element("tv", {
    "generator-info-name": "YUNIX CO EPG"
})

channel_ids = set()

for channel in channels:
    channel_id = channel["id"]

    if channel_id in channel_ids:
        raise ValueError("Duplicate channel ID")

    channel_ids.add(channel_id)

    ch = ET.SubElement(root, "channel", {
        "id": channel_id
    })

    ET.SubElement(ch, "display-name").text = channel["name"]

    if channel.get("logo"):
        ET.SubElement(ch, "icon", {
            "src": channel["logo"]
        })

for programme in schedule["programmes"]:
    if programme["channel"] not in channel_ids:
        raise ValueError("Unknown channel ID")

    p = ET.SubElement(root, "programme", {
        "start": programme["start"],
        "stop": programme["stop"],
        "channel": programme["channel"]
    })

    ET.SubElement(p, "title", {
        "lang": "tr"
    }).text = programme["title"]

    if programme.get("category"):
        ET.SubElement(p, "category", {
            "lang": "tr"
        }).text = programme["category"]

ET.indent(root, space="  ")

xml_data = ET.tostring(
    root,
    encoding="utf-8",
    xml_declaration=True
)

(BASE / "output" / "epg.xml").write_bytes(xml_data)

with gzip.open(BASE / "output" / "epg.xml.gz", "wb") as f:
    f.write(xml_data)

print("YUNIX CO EPG v0.1")
print("Channels:", len(channels))
print("Programmes:", len(schedule["programmes"]))
print("XML created!")
print("GZIP created!")
