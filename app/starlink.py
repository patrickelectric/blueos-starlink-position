import subprocess
from typing import Dict


class Starlink:

    def __init__(self):
        pass

    def position() -> Dict[str, float]:
        result = subprocess.run(
            [
                "python3",
                "starlink-grpc-tools/dish_grpc_text.py",
                "location",
                "--verbose",
            ],
            capture_output=True,
            text=True,
        )

        data = {}
        for line in result.stdout.splitlines():
            if ":" in line:
                key, value = line.split(":", 1)
                if not value:
                    return None
                data[key.strip()] = float(value.strip())

        return data


if __name__ == "__main__":
    star = Starlink()
    print(Starlink.position())
