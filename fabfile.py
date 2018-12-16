import os
from fabric.context_managers import lcd
from fabric.decorators import task
from fabric.operations import local
from fabric.colors import green

BASE_DIR = os.path.dirname(__file__)
FUNCTIONS_DIR = os.path.join(BASE_DIR, 'math_lambda')
TESTS_DIR = os.path.join(BASE_DIR, 'tests')
SLS = os.path.join(BASE_DIR, 'node_modules', 'serverless', 'bin', 'serverless')


@task
def check():
    """
    Static code checking
    """
    flake8_paths = [TESTS_DIR, FUNCTIONS_DIR, 'fabfile.py']
    with lcd(BASE_DIR):
        local('flake8 {}'.format(' '.join(flake8_paths)))


@task
def test():
    """
    Run all tests
    """
    with lcd(BASE_DIR):
        local('pytest')


@task
def package(stage='dev'):
    """
    Package up all of our functions (see serverless.yml)
    """
    opts = [
        '--cwd {}'.format(BASE_DIR),
        '--package {}-{}'.format(os.path.join(BASE_DIR, '.serverless'), stage)
    ]

    with lcd(BASE_DIR):
        local('{sls} package {opts}'.format(sls=SLS, opts=' '.join(opts)))


@task
def deploy(stage='dev'):
    """
    Deploy all of our functions, or just one (see serverless.yml)

    e.g: fab deploy
         fab deploy:dev
         fab deploy:stage=dev
         fab deploy:stage=dev,function=layout_to_store_graph
    """
    print(green('Deploying to {}'.format(stage)))

    opts = [
        '--stage {}'.format(stage),
        '--cwd {}'.format(BASE_DIR),
        '--region eu-west-1',
        '--package {}-{}'.format(os.path.join(BASE_DIR, '.serverless'), stage)
    ]

    if not os.getenv('CI', False):
        opts.append('--aws-profile {}'.format("personal"))

    with lcd(BASE_DIR):
        local('{sls} deploy {opts}'.format(sls=SLS, opts=' '.join(opts)))
        local('{sls} s3deploy {opts}'.format(sls=SLS, opts=' '.join(opts)))
