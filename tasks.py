import invoke


@invoke.task
def release(c):
    import utils_plus
    c.run('git push')
    c.run('git tag {}'.format(utils_plus.__version__))
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
    c.run("pylint utils_plus")
