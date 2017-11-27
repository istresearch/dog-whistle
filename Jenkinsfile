pipeline {
  agent any
  stages {
    stage('Test') {
      steps {
        sh '''# remove old build products


rm -f *.tar.gz'''
        sh '''# install package


python setup.py sdist
pip install dist/dog-whistle-*.tar.gz

'''
        sh '''# build package


mv dist/*.tar.gz .
rm -rf dist *.egg-info'''
        sh '''# Run tests


bash run_tests.sh'''
      }
    }
    stage('Build') {
      steps {
        sh '''# Copying package to pip repo
echo Copying package to pip repo


mkdir -p /data/blueocean/pip/prod
cp *.tar.gz /data/blueocean/pip/prod'''
      }
    }
  }
}