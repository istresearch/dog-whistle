def buildNumberInput;
node{
  stage('Get git branch'){
    gitBranchInput = input(
        id: 'gitBranch',
        message: 'dog-whistle git branch: ',
        ok: 'ok',
        parameters: [string(
          default: 'master',
          name: 'gitBranch'
        )]
    )
    echo ("Using branch " + gitBranchInput)
  }
  stage('Get Build Number'){
    buildNumberInput = input(
        id: 'buildNumber',
        message: 'dog-whistle build number: ',
        ok: 'ok',
        parameters: [string(
          description: 'The jenkins build number',
          name: 'buildNumber'
        )]
    )
    echo ("Fetching build #" + buildNumberInput)
  }
  stage('Copy Artifact'){
    def selector = [$class: 'SpecificBuildSelector', buildNumber: "${buildNumberInput}"];
    // dog-whistle-0.6.0.tar.gz
    step ([$class: 'CopyArtifact',
       projectName: "dog-whistle/joe-test-jenkinsfile",
       selector: selector,
       filter: 'dog-whistle-*.tar.gz']);
    sh 'ls -al'
  }
  stage('Deploy'){
    sh 'mv dog-whistle-*.tar.gz /data/blueocean/repo/pip/prod'
    echo 'Deplyed'
  }
}
