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
/bin/bash run_tests.sh'''
        sh '''# build package
mv dist/*.tar.gz .
rm -rf dist *.egg-info'''
      }
    }
    stage('Build') {
      steps {
        sh '''echo Copying package to pip repo
mkdir -p /data/blueocean/pip/prod
cp *.tar.gz /data/blueocean/pip/prod'''
      }
    }
  }
}