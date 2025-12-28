import hashlib
import pandas as pd

def df_sha256(df: pd.DataFrame) -> str:
    normalized = df.copy().sort_index(axis=1)
    normalized = normalized.sort_values(by=list(normalized.columns), kind="mergesort").reset_index(drop=True)

    data = normalized.to_csv(index=False).encode("utf-8")
    return hashlib.sha256(data).hexdigest()