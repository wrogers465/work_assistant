import pytest
from .context import classes
from lxml import html

    
@pytest.fixture
def email():
    email = classes.Email("Monitor Email", "Test", "Test", "wrogers465@gmail.com", "wrogers465@outlook.com")
    return email

# def test_inmate_class_that_it_parses_data_correctly_from_html(inmate):
#     assert inmate.docket == '1921091'

@pytest.fixture
def inmate(mocker):
    html_file = None
    with open("./tests/mock_data/docket_webpage.html") as f:
        html_file = html.fromstring(f.read())

    mocker.patch.object(classes.Inmate, '_get_html', return_value=html_file)
    inmate = classes.Inmate('1921091')
    return inmate

def test_inmate_dict(inmate):
    print(inmate.__dict__)
    assert inmate.__dict__['lname'] == 'Williams'


@pytest.mark.skip("Skipping so that an email isn't generated each time I test")
def test_create_email(email):
    email.create()