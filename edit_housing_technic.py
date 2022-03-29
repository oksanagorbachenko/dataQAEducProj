from great_expectations import DataContext
import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent


def validate_data(event, link):
    file_path = event[0]
    context = DataContext(os.path.join(BASE_DIR, 'great_expectations'))
    expectation_suite_name = "housing_technic"
    suite = context.get_expectation_suite(expectation_suite_name)
    suite.expectations = []

    batch_kwargs = {'data_asset_name': 'housing', 'datasource': 'pandas_s3',
                    'path': 's3a://fast-data-qa/' + file_path, 'link': link}
    batch = context.get_batch(batch_kwargs, suite)
    batch.head()

    batch.expect_column_values_to_not_be_null(column='longitude')
    batch.expect_table_column_count_to_equal(value=10)
    batch.expect_column_values_to_be_unique(column='longitude')
    batch.expect_column_values_to_not_be_null(column='total_bedrooms')
    batch.expect_column_values_to_be_of_type(column='latitude', type_='float64')
    batch.expect_column_to_exist(column='latitude')

    batch.save_expectation_suite(discard_failed_expectations=False)

    results = context.run_validation_operator("action_list_operator", assets_to_validate=[batch])

    validation_result_identifier = results.list_validation_result_identifiers()[0]
    return str(validation_result_identifier).replace('ValidationResultIdentifier::', ''), expectation_suite_name


# if __name__ == '__main__':
#     validate_data()
