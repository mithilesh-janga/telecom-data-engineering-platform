#To generate fake telecom call detail records

import uuid
import random
import csv
import json
from datetime import datetime,timedelta
from pathlib import Path

from utils.logger import get_logger
from utils.config import DATA_DIR

logger = get_logger(__name__)


def generate_msisdn() -> str:
    return "91"+"".join(str(random.randint(0,9))for _ in range(10))

def generate_cdr_record(call_date: datetime) ->dict:
    call_type = random.choice(["voice","sms"])
    duration = random.randint(10,3600) if call_type == "voice" else 0
    cost = round(duration * 0.01,2) if call_type == "voice" else 0.5

    return{
        "call_id": str(uuid.uuid4()),
        "caller_msisdn": generate_msisdn(),
        "receiver_msisdn": generate_msisdn(),
        "call_start_time": call_date.isoformat(),
        "call_duration_sec": duration,
        "call_type": call_type,
        "call_cost": cost,
    }

def generate_cdr_data(rows: int, call_date: datetime) -> list[dict]:
    logger.info(f"Generating {rows} CDR records for {call_date.date()}")
    return [generate_cdr_record(call_date) for _ in range(rows)]

def write_csv(data: list[dict], output_path: Path) -> None:
    with open(output_path, "w", newline="") as f:
        writer = csv.DictWriter(f,fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)

def write_json(data: list[dict], output_path: Path) -> None:
    with open(output_path, "w") as f:
        json.dump(data,f,indent=2)

def run(rows: int, call_date:datetime, file_format:str) -> None:
    DATA_DIR.mkdir(exist_ok=True)

    data = generate_cdr_data(rows, call_date)
    filename = f"cdr_{call_date.strftime('%Y%m%d')}.{file_format}"
    output_path = DATA_DIR / filename

    if file_format  == "csv":
        write_csv(data, output_path)
    elif file_format == "json":
        write_json(data, output_path)
    else:
        raise ValueError("Unsupported File Format")
    
    logger.info(f"CDR data written to {output_path}")


if __name__ == "__main__":
    run(
        rows = 1000,
        call_date=datetime.now() - timedelta(days=1),
        file_format="csv",
    )