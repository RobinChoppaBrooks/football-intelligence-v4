"""League ids for V5 from config/competitions.json names."""
import json, os
def league_ids(names):
    comp = json.load(open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "config", "competitions.json")))
    by = {c["name"]: c["league_id"] for c in comp["english"] + comp["european"]}
    return [by[n] for n in names]
