from dataclasses import dataclass
from typing import List

import pandas as pd


@dataclass
class OverallStatistics:
    evaluated_expectations: int
    successful_expectations: int
    unsuccessful_expectations: int
    success_percent: float


@dataclass
class GXResultBetweenOrInSetDetails:
    element_count: int
    unexpected_count: int
    unexpected_percent: float
    partial_unexpected_list: List
    missing_count: int
    missing_percent: float
    unexpected_percent_total: float
    unexpected_percent_nonmissing: float


@dataclass
class GXResultNotNullDetails:
    element_count: int
    unexpected_count: int
    unexpected_percent: float
    partial_unexpected_list: List


@dataclass
class AllResults:
    result_column_exist: bool = None
    result_not_null: GXResultNotNullDetails = None
    result_between_or_in_set: GXResultBetweenOrInSetDetails = None


@dataclass
class GXResultPerColumn:
    success: bool
    column: str
    all_results: AllResults


@dataclass
class CSVResult:
    encoding: bool
    format: bool


@dataclass
class ValidatedResult:
    file_path: str
    overall_result: bool
    overall_statistics: OverallStatistics = None
    csv_results: CSVResult = None
    parsed_results_gx: List[GXResultPerColumn] = None
    docs_urls: List = None
    final_df: pd.DataFrame = None
