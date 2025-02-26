from dataclasses import dataclass
from typing import List

import pandas as pd


@dataclass
class ResultDetails:
    element_count: int
    unexpected_count: int
    unexpected_percent: float
    partial_unexpected_list: List
    missing_count: int
    missing_percent: float
    unexpected_percent_total: float
    unexpected_percent_nonmissing: float


@dataclass
class DataPerColumn:
    success: bool
    column: str
    result: ResultDetails


@dataclass
class ValidatedResult:
    file_path: str
    parsed_results: List[DataPerColumn]
    overall_result: bool
    docs_urls: List
    final_df: pd.DataFrame
