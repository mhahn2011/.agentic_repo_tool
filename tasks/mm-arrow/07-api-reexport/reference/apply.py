import json, sys
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parents[2]))
import handref
handref.apply(json.loads((Path(__file__).parent / 'plan.json').read_text())['moves'])
