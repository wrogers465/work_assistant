import pytest
import uuid
from .context import db, classes


DATABASE_PATH = "./tests/mock_data/data.db"

@pytest.fixture
def email():
    email = classes.Email("{} w/ {} {}", "Docket: {}", "wrogers465@gmail.com", "wrogers465@outlook.com", name="Monitor Email", function="monitor_email")
    return email

@pytest.fixture
def database():
    database = db.Database()
    return database

def test_getting_email_options_ordered_by_most_used(database):
    email_options = database.get_email_options()
    print(email_options)

def test_getting_email_by_template_name(database):
    email_data= database.get_email_by_template_name('Savanna fox')
    print(email_data)
    assert dict(email_data)['id'] == 11

def test_that_email_is_saved(database):
    template_name = str(uuid.uuid4())
    email_data = {"template_name": template_name,
                  "subject": "Test",
                  "body": "Test",
                  "receiver": "wrogers465@gmail.com",
                  "cc": "wrogers465@outlook.com",
                  "func": "test"}
    
    database.save_email(email_data)
    result = database.get_email_by_template_name(template_name)
    assert result["template_name"] == template_name


@pytest.mark.skip("Skipping so that a new database isn't created each test")
def test_that_db_is_created(mocker):
    mocker.patch("src.db.DATABASE_PATH", DATABASE_PATH)
    db.init_db()


