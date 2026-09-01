""" 

Shared safety net for writing DataFrames to Parquet. 

  

LLM-generated SQL occasionally produces column types that pandas/pyarrow 

can't serialize automatically -- DuckDB's UUID(), DECIMAL, INTERVAL, and 

similar types come back as native Python objects (uuid.UUID, Decimal, etc.) 

that pyarrow's type inference doesn't recognize. Rather than let any agent 

crash on to_parquet(), this coerces any column containing such objects to 

a plain string, which Parquet always handles. 

""" 

import pandas as pd 

  

  

def sanitize_for_parquet(df: pd.DataFrame) -> pd.DataFrame: 

    for col in df.columns: 

        if df[col].dtype != object: 

            continue 

        sample = df[col].dropna() 

        if sample.empty: 

            continue 

        first_val = sample.iloc[0] 

        # Anything that isn't a plain Python str/int/float/bool is suspect -- 

        # UUID, Decimal, date/time subtypes DuckDB sometimes returns, etc. 

        if not isinstance(first_val, (str, int, float, bool)): 

            df[col] = df[col].astype(str) 

    return df 