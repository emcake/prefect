import sys
import pytest

import prefect
from prefect.utilities import plugins


class TestAPIRegistry:
    def test_register_function(self):
        @plugins.register_api("tests.my_fn")
        def f(x):
            return x + 1

        assert prefect.api.tests.my_fn is f

    def test_overwrite_function(self):
        @plugins.register_api("tests.my_fn")
        def f(x):
            return x + 1

        @plugins.register_api("tests.my_fn")
        def g(x):
            return x + 100

        assert prefect.api.tests.my_fn is g

    def test_overwritten_function_is_respected_at_runtime(self):
        @plugins.register_api("tests.my_fn")
        def f(x):
            return x + 1

        def add(x):
            return prefect.api.tests.my_fn(x)

        assert add(1) == 2

        @plugins.register_api("tests.my_fn")
        def g(x):
            return x + 100

        assert add(1) == 101
