
import pdfplumber
import pandas as pd
from typing import Optional

SCHEMA = ['Date', 'Description', 'Debit Amt', 'Credit Amt', 'Balance']

def parse(pdf_path: str) -> Optional[pd.DataFrame]:
    try:
        rows = []
        with pdfplumber.open(pdf_path) as pdf:
            for page in pdf.pages:
                tables = page.extract_tables()
                for table in tables or []:
                    for row in table or []:
                        if not row:
                            continue
                        first = str(row[0]).strip() if row[0] is not None else ""
                        if first.lower().startswith("date") or "bank statement" in "".join(map(str,row)).lower():
                            continue
                        row = list(row)[:len(SCHEMA)]
                        while len(row) < len(SCHEMA):
                            row.append(None)
                        rows.append(row)

        df = pd.DataFrame(rows, columns=SCHEMA)

        # Keep string columns as strings, numeric columns as float
        for col in df.columns:
            if col.lower() in ['date', 'description']:
                df[col] = df[col].astype(str)
            else:
                df[col] = pd.to_numeric(df[col].astype(str).str.replace(',', ''), errors='coerce')

        return df
    except FileNotFoundError:
        raise
    except Exception as e:
        raise RuntimeError(f"Local fallback parser failed: {e}")
