def buildNumberInput;
node{
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
    def selector = [$class: 'SpecificBuildSelector', buildNumber: "${buildNumber}"];
    // dog-whistle-0.6.0.tar.gz
    step ([$class: 'CopyArtifact',
       projectName: "dog-whistle",
       selector: selector,
       filter: 'dog-whistle-*.tar.gz']);
    sh 'ls -al'
  }
}
