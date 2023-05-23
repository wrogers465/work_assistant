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
    email_data = database.get_email_by_template_name("Monitor Email")
    database.close()
    return email_data

@pytest.fixture
def mock_inmate(mocker):
    html_file = None
    with open("./tests/mock_data/docket_webpage.html") as f:
        html_file = html.fromstring(f.read())

    mocker.patch.object(classes.Inmate, '_get_html', return_value=html_file)
    inmate = classes.Inmate('1921091')
    return inmate

def test_email_factory(mock_inmate, mock_email_data):
    email_data = mock_email_data
    # email_data = {'id': 11, 'template_name': 'Savanna fox', 'subject': 'budgetary management', 'body': 'Curabitur in libero ut massa volutpat convallis. Morbi odio odio, elementum eu, interdum eu, tincidunt in, leo. Maecenas pulvinar lobortis est. Phasellus sit amet erat. Nulla tempus. Vivamus in felis eu sapien cursus vestibulum. Proin eu mi. Nulla ac enim. In tempor, turpis nec euismod scelerisque, quam turpis adipiscing lorem, vitae mattis nibh ligula nec sem.', 'receiver': 'kbenedictea@npr.org', 'cc': 'sramarda@yelp.com', 'func': 'Peso', 'number_of_uses': 98}
    email = functions.email_factory("1932345", email_data)
    email.create()

@pytest.mark.skip("Skipping so that an email isn't generated each time I test")
def test_create_email(email):
    email.create()