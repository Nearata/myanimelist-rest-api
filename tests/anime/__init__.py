from requests import Session

from mal.main import create_app


app = create_app()
app.state.session = Session()
