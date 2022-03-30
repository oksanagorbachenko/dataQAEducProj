from edit_housing import validate_data as edit_housing_validate_data
from edit_housing_technic import validate_data as edit_housing_technic_validate_data
from test_pandas_profiler import profile_data
import re


def handler(event, cloudfront):
    profiling_link = profile_data(event, 2)
    technic_test_suite_identifier, technic_test_suite = edit_housing_technic_validate_data(event, profiling_link)
    business_test_suite_identifier, business_test_suite = edit_housing_validate_data(event, profiling_link)
    technic_test_suite_link = 'https://d35b8h21obf2t9.cloudfront.net/validations/' + technic_test_suite_identifier + '.html'
    business_test_suite_link = 'https://d35b8h21obf2t9.cloudfront.net/validations/' + business_test_suite_identifier + '.html'
    suites = [technic_test_suite, business_test_suite]

    # file_path = event[0]
    match = re.search('.+(\/)(.*?).parquet', "data/housing/housing.parquet")
    file_name = re.search('[^_]*', match.group(2))
    file = file_name.group(0)


    result = {
        # "path": file_path,
        "file": file,
        "profiling": profiling_link[-1],
        "technic_test_suite": technic_test_suite_link,
        "business_test_suite": business_test_suite_link,
        "suites": suites
    }
    return result
