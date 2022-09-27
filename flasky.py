from app import create_app
from infrastructure.models.roles import Role

app = create_app('testing')


@app.shell_context_processor
def make_shell_context():
    return {'role': Role, 'app': app}
