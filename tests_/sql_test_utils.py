import os

import pytest

from tests_.execute_sql_files import execute_sql_files


def run_sql_test(sql_dir, test_cases, exclude_limit_files=None):
    if exclude_limit_files is None:
        exclude_limit_files = set()

    @pytest.mark.parametrize("filename, params", test_cases)
    def test_sql(filename, params):
        sql_file_path = os.path.join(sql_dir, filename)

        with open(sql_file_path, 'r') as sql_file:
            zapytanie = sql_file.read()

        for key, value in params.items():
            zapytanie = zapytanie.replace(key, value)

        if filename not in exclude_limit_files:
            zapytanie += " limit 1"

        execute_sql_files(zapytanie, filename)

    return test_sql
