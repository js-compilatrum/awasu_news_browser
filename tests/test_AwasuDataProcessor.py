import pandas as pd
from manipulators import AwasuDataProcessor

awasu = AwasuDataProcessor()

CONCEPT_DEBUG = True
CSV_TEST_DATA = 'test_data.json'
#https://datatest.readthedocs.io/en/stable/how-to/fixtures/dataframe-fixture.html

def test_create_df():
    # assert type(awasu.create_df()) is pd.DataFrame()
    assert awasu.create_df() != -1
