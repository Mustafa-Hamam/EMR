import pandas as pd
from report_core.report import auth_snflk,monthly_cases_overview
def test():
    df = monthly_cases_overview(auth_snflk())
    assert isinstance(df, pd.DataFrame), "Function should return a pandas DataFrame"
    assert not df.empty, "DataFrame should not be empty"