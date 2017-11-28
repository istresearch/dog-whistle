pipeline {
  agent {
      docker { image 'python:2.7' }
  }
  stages {
    stage('Install package'){
      steps{
        sh 'hostname'
        sh 'python setup.py sdist'
        sh 'pip install dist/dog-whistle-*.tar.gz'
      }
    }
    stage('Test') {
      steps {
        sh 'hostname'
        sh 'bash run_tests.sh'
      }
    }
    stage('Deploy') {
      steps {
        sh 'hostname'
        sh 'mv dist/*.tar.gz .'
        sh 'rm -rf dist *.egg-info'
        sh 'mkdir -p /data/blueocean/repo/pip/prod'
        sh 'cp *.tar.gz /data/blueocean/repo/pip/prod'
      }
    }
  }
}
