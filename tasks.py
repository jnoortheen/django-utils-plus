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

    # [pypi]
    # repository: https://upload.pypi.org/legacy/
    # username: jnoortheen
    # password: pwd
    c.run('python setup.py sdist upload')


@invoke.task
def test(c):
    c.run(
        'pytest '
        '--cov utils_plus '
        '--cov-report term-missing '
        '--cov-report term:skip-covered '
    )
