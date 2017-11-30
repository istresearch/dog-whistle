node{
  checkout scm
}

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
      sh 'mv dist/dog-whistle-*.tar.gz .'
      archive 'dog-whistle-*.tar.gz'
  }
}
