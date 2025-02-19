from dataclasses import dataclass
from typing import List

import pandas as pd


@dataclass
class ValidatedResult:
    parsed_results: List
    overall_result: bool
    docs_urls: List
    final_df: pd.DataFrame
