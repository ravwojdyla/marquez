from typing import Type, Optional, Dict

from airflow.contrib.operators.bigquery_operator import BigQueryOperator
from airflow.models import BaseOperator
from airflow.operators.postgres_operator import PostgresOperator
from great_expectations_provider.operators.great_expectations import GreatExpectationsOperator

from marquez_airflow.extractors import BaseExtractor
from marquez_airflow.extractors.bigquery_extractor import BigQueryExtractor
from marquez_airflow.extractors.great_expectations_extractor import GreatExpectationsExtractor
from marquez_airflow.extractors.postgres_extractor import PostgresExtractor


class Extractors:
    def __init__(self):
        self.extractors = {
            PostgresOperator: PostgresExtractor,
            BigQueryOperator: BigQueryExtractor,
            GreatExpectationsOperator: GreatExpectationsExtractor
            # Append new extractors here
        }
    
        self.patchers = {
            GreatExpectationsOperator: GreatExpectationsExtractor
        }

    def get_extractor_class(self, clazz: Type) -> Optional[Type[BaseExtractor]]:
        if clazz in self.extractors:
            return self.extractors[clazz]
        return None

    def get_patcher_class(self, clazz: Type) -> Optional[Type[BaseExtractor]]:
        if clazz in self.patchers:
            return self.patchers[clazz]
        return None
