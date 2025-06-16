import invoke


@invoke.task
def test(c):
    c.run(
        'pytest '
        '--cov utils_plus '
    )

 
@invoke.task
def lint(c):
    c.run("ruff check . --fix")
    c.run("mypy utils_plus")
