"""Optional native Croissant consumer check; not a runtime dependency.

Run: uv run --with mlcroissant==1.1.1 python scripts/check_croissant.py
"""

from pathlib import Path

import mlcroissant as mlc


def main():
    path = Path("build/benchmark-v1/croissant.json")
    dataset = mlc.Dataset(jsonld=path)
    if len(dataset.metadata.record_sets) != 2:
        raise ValueError("expected two independent split RecordSets")
    print("PASS: mlcroissant 1.1.1 native parser, two split RecordSets")


if __name__ == "__main__":
    main()
