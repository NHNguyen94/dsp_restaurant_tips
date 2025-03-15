from dataclasses import dataclass
from typing import List

import pandas as pd


@dataclass
class FailureMode:
    failure_mode: str
    count: int


@dataclass
class FailureModePerColumn:
    column: str
    failure_mode: FailureMode


@dataclass
class OverallStatistics:
    evaluated_expectations: int
    successful_expectations: int
    unsuccessful_expectations: int
    success_percent: float
    rows_count: int = None
    bad_rows_count: int = None
    bad_rows_percent: float = None
    failure_modes: List[FailureModePerColumn] = None


@dataclass
class GXResultBetweenOrInSetDetails:
    result: bool
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
    result: bool
    element_count: int
    unexpected_count: int
    unexpected_percent: float
    partial_unexpected_list: List


@dataclass
class GXResultBeOfTypeDetails:
    result: bool
    observed_value: str = None  # This only appears in float column, due to great expectation lib, and the other fields will be None
    element_count: int = None
    unexpected_count: int = None
    unexpected_percent: float = None
    partial_unexpected_list: List = None
    missing_count: int = None
    missing_percent: float = None
    unexpected_percent_total: float = None
    unexpected_percent_nonmissing: float = None


@dataclass
class AllResults:
    result_column_exist: bool = None
    result_not_null: GXResultNotNullDetails = None
    result_be_of_type: GXResultBeOfTypeDetails = None
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
    empty_file: bool = None


@dataclass
class ValidatedResult:
    file_path: str
    overall_result: bool
    overall_statistics: OverallStatistics = None
    csv_results: CSVResult = None
    parsed_results_gx: List[GXResultPerColumn] = None
    docs_urls: List = None
    final_df: pd.DataFrame = None
