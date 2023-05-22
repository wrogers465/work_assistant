from .context import functions


def test_email_factory():
    docket = '1921091'
    email_data = {'id': 11, 'template_name': 'Savanna fox', 'subject': 'budgetary management', 'body': 'Curabitur in libero ut massa volutpat convallis. Morbi odio odio, elementum eu, interdum eu, tincidunt in, leo. Maecenas pulvinar lobortis est. Phasellus sit amet erat. Nulla tempus. Vivamus in felis eu sapien cursus vestibulum. Proin eu mi. Nulla ac enim. In tempor, turpis nec euismod scelerisque, quam turpis adipiscing lorem, vitae mattis nibh ligula nec sem.', 'receiver': 'kbenedictea@npr.org', 'cc': 'sramarda@yelp.com', 'func': 'Peso', 'number_of_uses': 98}
    email = functions.email_factory(docket, email_data)