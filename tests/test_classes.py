import pytest
from .context import classes, functions, db
from lxml import html

    
@pytest.fixture
def email():
    email = classes.Email("Monitor Email", "Test", "Test", "wrogers465@gmail.com", "wrogers465@outlook.com")
    return email

@pytest.fixture
def mock_email_data():
    database = db.Database()
    email_data = database.get_email_by_template_name("Information Filed")
    database.close()
    return email_data

@pytest.fixture
def mock_inmate(mocker):
    html_file = None
    with open("./tests/mock_data/docket_webpage.html") as f:
        html_file = html.fromstring(f.read())

    mocker.patch.object(classes.Inmate, '_get_html', return_value=html_file)

    inmate = classes.Inmate('1874567')
    return inmate


def test_inmate_charges(mock_inmate):
    inmate = mock_inmate
    assert inmate.charges == [{'Agency Report Number': 'SO21055150', 'Offense Description': 'SALE OR DELIVERY OF CRACK COCAINE', 'Statute': '893.13(1)(A)(1)/F', 'Amended Charge Desc.': None, 'Amended Charge Statute': None, 'Court Case Number': '21-08792-CF-1', 'Bond Assessed': '$7,500.00', 'Bond Amount Due': '$0.00', 'Charge Status': 'BONDED OUT', 'Arrest Type': 'ON VIEW', 'OBTS': '5210112013'}, {'Agency Report Number': 'SO21055150', 'Offense Description': 'POSSESSION OF CRACK COCAINE', 'Statute': '893.13(6)(A)/F', 'Amended Charge Desc.': None, 'Amended Charge Statute': None, 'Court Case Number': '21-08792-CF-2', 'Bond Assessed': '$2,000.00', 'Bond Amount Due': '$0.00', 'Charge Status': 'BONDED OUT', 'Arrest Type': 'ON VIEW', 'OBTS': '5210112013'}]


def test_email_factory(mock_inmate, mock_email_data):
    email_data = mock_email_data
    email = functions.email_factory("1874567", email_data)
    email.create()

@pytest.mark.skip("Skipping so that an email isn't generated each time I test")
def test_create_email(email):
    email.create()