# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
import functools

from great_expectations_provider.operators.great_expectations import GreatExpectationsOperator
from typing import Optional
from functools import partial

from marquez_airflow.extractors import (
    BaseExtractor,
    StepMetadata,
)


def wrap_callback(f):
    @functools.wraps(f)
    def wrapper(self, *args, **kwargs):
        result = f(self, *args, **kwargs)
        self._extractor.store_result(result)
        return result
    return wrapper


GreatExpectationsOperator.execute = wrap_callback(GreatExpectationsOperator.execute)


class GreatExpectationsExtractor(BaseExtractor):
    operator_class = GreatExpectationsOperator

    def __init__(self, operator):
        super().__init__(operator)
        self.operator._extractor = self
        self.result = None

    def store_result(self, result):
        self.result = result

    def parse_result(self):
        with open('/home/mobuchowski/result.txt', 'a') as f:
            f.write('test\n')

    def extract(self) -> Optional[StepMetadata]:
        if self.result:
            self.parse_result()
            return StepMetadata(name='name')
        return None

    def extract_on_complete(self, task_instance) -> Optional[StepMetadata]:
        if self.result:
            self.parse_result()
