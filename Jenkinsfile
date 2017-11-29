docker.image('python:2.7').inside {
  stage('Install package'){
      sh 'hostname'
      sh 'python setup.py sdist'
      sh 'pip install dist/dog-whistle-*.tar.gz'
  }
  stage('Test') {
      sh 'hostname'
      sh 'bash run_tests.sh'
  }
  stage('Archive Artifact') {
      archive 'dist/dog-whistle-*.tar.gz'
  }
}
