pipeline {
  agent any
  stages {
    stage('Build') {
      steps {
        sh '''# remove old build products
rm -f *.tar.gz'''
        sh '''# install package
python setup.py sdist
'''
        sh '''# pip install

pip install dist/dog-whistle-*.tar.gz'''
      }
    }
    stage('Test') {
      steps {
        sh 'bash run_tests.sh'
      }
    }
    stage('Deploy') {
      steps {
        sh '''echo Copying package to pip repo
mkdir -p /data/blueocean/repo/pip/prod
cp *.tar.gz /data/blueocean/repo/pip/prod'''
      }
    }
  }
}