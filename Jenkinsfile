pipeline {
    agent any

    environment {
        // Adresse du serveur Playwright (docker-compose.yml) vue depuis Jenkins.
        // Pour la trouver : ip addr show docker0 | grep inet
        PLAYWRIGHT_SERVER = 'ws://172.17.0.1:3000/'
        // Environnement ciblé (fichier environments/<ENV>.env)
        ENV = 'demo'
        // uv est installé dans ~/.local/bin par l'étape "Install uv"
        PATH = "${env.HOME}/.local/bin:${env.PATH}"
    }

    stages {
        stage('Clean Workspace & Checkout') {
            steps {
                cleanWs()
                checkout scm
            }
        }

        stage('Install uv') {
            steps {
                // Seul prérequis de l'agent : uv. Il télécharge lui-même la bonne version de Python.
                sh 'command -v uv || curl -LsSf https://astral.sh/uv/install.sh | sh'
            }
        }

        stage('Install Dependencies') {
            steps {
                // --frozen : installe exactement les versions de uv.lock, échoue s'il n'est pas à jour
                sh 'uv sync --frozen'
            }
        }

        stage('Lint') {
            steps {
                sh 'uv run ruff check .'
                sh 'uv run ruff format --check .'
            }
        }

        stage('Type Check') {
            steps {
                sh 'uv run mypy'
            }
        }

        stage('Run Tests') {
            steps {
                // Identifiants injectés depuis Jenkins > Credentials (type "Username with password")
                withCredentials([
                    usernamePassword(
                        credentialsId: 'playwright-customer',
                        usernameVariable: 'CUSTOMER_EMAIL',
                        passwordVariable: 'CUSTOMER_PASSWORD'
                    ),
                    usernamePassword(
                        credentialsId: 'playwright-admin',
                        usernameVariable: 'ADMIN_EMAIL',
                        passwordVariable: 'ADMIN_PASSWORD'
                    )
                ]) {
                    // Pas de "playwright install" : les navigateurs sont sur le serveur Playwright
                    sh '''
                        uv run pytest \
                            -n 4 \
                            --reruns 2 \
                            --junitxml=reports/junit.xml \
                            --html=reports/report.html --self-contained-html \
                            --alluredir=allure-results
                    '''
                }
            }
        }
    }

    post {
        always {
            // Tendance des résultats dans Jenkins
            junit allowEmptyResults: true, testResults: 'reports/junit.xml'
            publishHTML(target: [
                allowMissing: true,
                alwaysLinkToLastBuild: true,
                keepAll: true,
                reportDir: 'reports',
                reportFiles: 'report.html',
                reportName: 'Rapport pytest'
            ])
            allure([
                includeProperties: false,
                jdk: '',
                reportBuildPolicy: 'ALWAYS',
                results: [[path: 'allure-results']]
            ])
            // Traces, captures et vidéos des tests en échec
            archiveArtifacts artifacts: 'test-results/**', allowEmptyArchive: true
        }
    }
}
