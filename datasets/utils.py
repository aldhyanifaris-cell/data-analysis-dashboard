"""
Datasets utility module: Robust file loaders and dataset profilers using Pandas.
"""
import os
import io
import json
import pandas as pd
import numpy as np
from typing import Tuple, Dict, Any, List

def load_dataframe_from_file(file_path: str, file_format: str = 'csv') -> pd.DataFrame:
    """Safely load a pandas DataFrame from file path supporting multiple formats."""
    ext = file_format.lower()
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")

    if ext in ['csv', 'txt']:
        try:
            return pd.read_csv(file_path, encoding='utf-8')
        except UnicodeDecodeError:
            return pd.read_csv(file_path, encoding='latin1')
    elif ext in ['xlsx', 'xls']:
        return pd.read_excel(file_path)
    elif ext == 'json':
        try:
            return pd.read_json(file_path)
        except ValueError:
            with open(file_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            return pd.json_normalize(data)
    elif ext == 'parquet':
        return pd.read_parquet(file_path)
    else:
        # Fallback detection
        try:
            return pd.read_csv(file_path)
        except Exception:
            return pd.read_excel(file_path)

def profile_and_extract_metadata(df: pd.DataFrame) -> Tuple[Dict[str, Any], List[Dict[str, Any]], Dict[str, Any]]:
    """Extract metadata, column profiles, and sample data from a DataFrame."""
    row_count, col_count = df.shape
    total_cells = row_count * col_count if row_count and col_count else 1
    missing_cells = int(df.isna().sum().sum())
    missing_percentage = float(round((missing_cells / total_cells) * 100, 2))
    duplicate_rows = int(df.duplicated().sum())
    memory_usage = int(df.memory_usage(deep=True).sum())

    dataset_meta = {
        'row_count': row_count,
        'column_count': col_count,
        'missing_cells_count': missing_cells,
        'missing_cells_percentage': missing_percentage,
        'duplicate_rows_count': duplicate_rows,
        'memory_usage_bytes': memory_usage,
    }

    columns_meta = []
    for idx, col in enumerate(df.columns):
        series = df[col]
        null_c = int(series.isna().sum())
        null_p = float(round((null_c / row_count) * 100, 2)) if row_count else 0.0
        unique_c = int(series.nunique(dropna=True))
        unique_p = float(round((unique_c / row_count) * 100, 2)) if row_count else 0.0

        raw_dtype = str(series.dtype)
        # Determine logical type
        if pd.api.types.is_numeric_dtype(series):
            if pd.api.types.is_bool_dtype(series):
                data_type = 'boolean'
            else:
                data_type = 'numeric'
        elif pd.api.types.is_datetime64_any_dtype(series):
            data_type = 'datetime'
        elif pd.api.types.is_bool_dtype(series):
            data_type = 'boolean'
        elif unique_c < max(20, row_count * 0.05):
            data_type = 'categorical'
        else:
            data_type = 'text'

        col_dict: Dict[str, Any] = {
            'name': str(col),
            'data_type': data_type,
            'raw_dtype': raw_dtype,
            'column_index': idx,
            'null_count': null_c,
            'null_percentage': null_p,
            'unique_count': unique_c,
            'unique_percentage': unique_p,
            'top_values_json': {},
            'min_value': None,
            'max_value': None,
            'mean_value': None,
            'median_value': None,
            'std_dev': None,
            'skewness': None,
            'kurtosis': None,
        }

        if data_type == 'numeric':
            clean_s = series.dropna()
            if len(clean_s) > 0:
                col_dict['min_value'] = float(clean_s.min())
                col_dict['max_value'] = float(clean_s.max())
                col_dict['mean_value'] = float(round(clean_s.mean(), 4))
                col_dict['median_value'] = float(round(clean_s.median(), 4))
                col_dict['std_dev'] = float(round(clean_s.std(), 4)) if len(clean_s) > 1 else 0.0
                try:
                    col_dict['skewness'] = float(round(clean_s.skew(), 4))
                    col_dict['kurtosis'] = float(round(clean_s.kurtosis(), 4))
                except Exception:
                    pass

        # Top values for categorical/text
        top_val_series = series.value_counts(dropna=True).head(10)
        col_dict['top_values_json'] = {str(k): int(v) for k, v in top_val_series.items()}
        columns_meta.append(col_dict)

    # Clean samples for JSON serialization (convert NaN to None)
    clean_df = df.fillna("")
    head_rows = clean_df.head(20).to_dict(orient='records')
    tail_rows = clean_df.tail(20).to_dict(orient='records')
    random_sample = clean_df.sample(min(20, row_count)).to_dict(orient='records') if row_count > 0 else []

    sample_meta = {
        'head_rows_json': head_rows,
        'tail_rows_json': tail_rows,
        'random_sample_json': random_sample,
    }

    return dataset_meta, columns_meta, sample_meta
