pipeline {
    agent { label 'gcp-node' }

    environment {
        GOOGLE_APPLICATION_CREDENTIALS = "serious-hall-459619-j3-fec998871be2.json"
    }
    
    parameters {
        string(name: 'Question', defaultValue: 'What is 5G?', description: 'Name of the PDF file to process')
        booleanParam(name: 'SkipUpdate', defaultValue: false, description: 'Do you want to skip the update and generate the answer directly?')
    }
    stages {
        stage("Check and Install Ollama"){ 
            when{
                expression { return !params.SkipUpdate}
            }
            steps{
                sh '''
                    if ! command -v ollama >/dev/null 2>&1; then
                        echo "Installing Ollama..."
                        curl -fsSL https://ollama.com/install.sh | sh
                    else
                        echo "Ollama is already installed."
                    fi
                '''
            }
        }

        stage('Pulling LLM'){
            when{
                expression { return !params.SkipUpdate}
            }
            steps {
                sh '''
                    if ollama list | grep -q llama3; then
                        echo "llama3 already pulled."
                    else
                        echo "Pulling llama3..."
                        ollama pull llama3
                    fi
                '''
            }
        }

        stage('Checkout') {
            when{
                expression { return !params.SkipUpdate}
            }
            steps {
                git url: 'https://github.com/changliu8/GCP_RAG.git', branch: 'main'
            }
        }
        
        stage('Creating Virtual Environment'){
            when{
                expression { return !params.SkipUpdate}
            }
            steps{
                sh "python3.8 -m venv RAG"
            }
        }
        
        stage('Install dependencies') {
            when{
                expression { return !params.SkipUpdate}
            }
            steps {
                sh '''
                    . ${WORKSPACE}/RAG/bin/activate
                    python3.8 -m pip install --upgrade pip
                    python3.8 -m pip install -r requirements.txt
                '''
            }
        }

        stage('Setup GCP Credential') {
            when{
                expression { return !params.SkipUpdate}
            }
            steps {
                withCredentials([file(credentialsId: 'gcp-storage', variable: 'GCP_KEY')]) {
                    sh '''
                    if [ ! -f "$WORKSPACE/serious-hall-459619-j3-fec998871be2.json" ]; then
                        cp "$GCP_KEY" "$GOOGLE_APPLICATION_CREDENTIALS"
                        echo "Credential copied."
                    else
                        echo "Credential already exists. Skipping copy."
                    fi
                    '''
                }
            }
        }
        
        stage('Download files') {
            when{
                expression { return !params.SkipUpdate}
            }
            steps {
                sh '''
                    . ${WORKSPACE}/RAG/bin/activate
                    python3.8 download_faiss.py
                '''
            }
        }
        
        stage("Generating answers"){
            steps{
                sh '''
                    . ${WORKSPACE}/RAG/bin/activate
                    python3.8 gcp_rag.py "$Question"
                '''
            }
        }
    }
}