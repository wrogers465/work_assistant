import pytest
import os
import time
from .context import create_db, create_email, get_initial_email_data


MOCK_DATA_PATH = "./tests/mock_data/data.db"


@pytest.mark.skip()
def test_that_db_is_created(mocker):
    mocker.patch("src.functions.DATABASE_PATH", MOCK_DATA_PATH)
    os.remove(MOCK_DATA_PATH)
    time.sleep(2)
    create_db()
    assert os.path.isfile(MOCK_DATA_PATH)


def test_get_initial_email_data(mocker):
    mocker.patch("src.functions.DATABASE_PATH", MOCK_DATA_PATH)
    email_names, initial_email = get_initial_email_data()
    assert (email_names[0], initial_email[6]) == ("Sub-Ex", "#c3207c")


@pytest.mark.skip()
def test_create_email():
    create_email()

