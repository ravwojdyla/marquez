"""
Unittest module to test Great Expectations Operators.

Requires the unittest, pytest, and requests-mock Python libraries.
pip install google-cloud-storage

Run test:

    python3 -m unittest test.operators.test_operators.TestGreatExpectationsOperator

"""

from pathlib import Path
import logging
import os

from marquez_airflow.extractors.great_expectations_extractor import GreatExpectationsExtractor

from great_expectations_provider.operators.great_expectations import GreatExpectationsOperator


log = logging.getLogger(__name__)

# Set relative paths for Great Expectations directory and sample data
base_path = Path(__file__).parents[0]
data_file = os.path.join(base_path,
                         'include',
                         'data/yellow_tripdata_sample_2019-01.csv')
ge_root_dir = os.path.join(base_path, 'include', 'great_expectations')


def test_great_expectations_operator_batch_kwargs_success():
    operator = GreatExpectationsOperator(
        task_id='ge_batch_kwargs_pass',
        expectation_suite_name='taxi.demo',
        batch_kwargs={
            'path': data_file,
            'datasource': 'data__dir'
        },
        data_context_root_dir=ge_root_dir
    )

    extractor = GreatExpectationsExtractor(operator)

    result = operator.execute({})

    metadata = extractor.extract()
    log.info(result)

    assert result['success']



