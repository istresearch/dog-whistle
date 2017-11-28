docker.image('python:2.7').inside {
  stage('Install package'){
      sh 'hostname'
      sh 'python setup.py sdist'
      sh 'pip install dist/dog-whistle-*.tar.gz'
  }
  stage('Test') {
      sh 'hostname'
      sh 'bash run_tests.sh'
      stash includes: '*.tar.gz', name: 'built'
  }
  milestone()
  input 'Continue to deploy stage?'
  stage('Deploy') {
      sh 'hostname'
      sh 'mv dist/*.tar.gz .'
      sh 'rm -rf dist *.egg-info'
      sh 'mkdir -p /data/blueocean/repo/pip/prod'
      sh 'cp *.tar.gz /data/blueocean/repo/pip/prod'
  }
}
