pipeline {
  agent any
  stages {
    stage('Remove old build products') {
      steps{
        sh 'rm -f *.tar.gz'
      }
    }
    stage('Install package'){
      steps{
        sh 'python setup.py sdist'
        sh 'pip install dist/dog-whistle-*.tar.gz'
      }
    }
    stage('Test') {
      steps {
        sh 'bash run_tests.sh'
      }
    }
    stage('Deploy') {
      steps {
        sh 'mv dist/*.tar.gz .'
        sh 'rm -rf dist *.egg-info'
        sh 'mkdir -p /data/blueocean/repo/pip/prod'
        sh 'cp *.tar.gz /data/blueocean/repo/pip/prod'
      }
    }
  }
}
