import invoke


@invoke.task
def release(c):
    cversion: invoke.Result = c.run("poetry version")
    version: str = cversion.stdout.replace("django-utils-plus", "").strip()
    c.run('git push')
    c.run('git tag v{}'.format(version))
    c.run('git push --tags')

    # dont forget to have this file
    # ~/.pypirc
    # [distutils]
    # index-servers =
    #  pypi

    c.run('poetry publish --build')


@invoke.task
def test(c):
    c.run(
        'pytest '
        '--cov utils_plus '
    )


@invoke.task
def lint(c):
    c.run("mypy utils_plus")
    c.run("ruff check . --fix")
