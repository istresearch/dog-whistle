node{
  stage('Get Build Number'){
    def buildNumberInput = input(
        id: 'buildNumber', message: 'dog-whistle build number: ', ok: 'ok', parameters: [string(description: 'The jenkins build number', name: 'buildNumber')]
    )
    echo ("Fetching build #" + buildNumberInput)
  }
}
