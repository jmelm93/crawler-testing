#!/bin/sh

APP_NAME="swf-crawlers"                          # name of the application
PROJECT_ID="XXXXXXXXXXXXX"                       # Google Cloud Project ID
CURRENT_DATE_TIME=$(date +%Y-%m-%d-%H-%M)        # e.g. 2020-01-01-12-00
BUILD_TAG="build_${CURRENT_DATE_TIME}"           # Build Tag: e.g., build_2022-07-10-04-01
REGION="us-central1"                             # Google Cloud region
TIMEOUT="60m"                                    # Timeout for the deployment - timeout max for cloudrun is 60 minutes          
MEMORY="16Gi"                                    # Memory for the deployment - 1Gi memory is the default for Cloud Run
CPU="4"                                          # CPU for the deployment - 1Gi CPU is the default for Cloud Run (1Gi = 1 core)


echo "--------------------------------------------------------------------------------"
echo "Building the Docker image to push to Google Container Registry ..."
echo "--------------------------------------------------------------------------------"
gcloud builds submit --tag gcr.io/${PROJECT_ID}/${APP_NAME}:${BUILD_TAG} . 

if [ $? -eq 0 ]; then # if build is successful, then push the image to gcr.io
    echo "--------------------------------------------------------------------------------"
    echo "Build succeeded. Deploying the image to Cloud Run ..."
    echo "--------------------------------------------------------------------------------"
    gcloud run deploy ${APP_NAME} --platform managed --image=gcr.io/${PROJECT_ID}/${APP_NAME}:${BUILD_TAG} --region=${REGION} --timeout=${TIMEOUT} --memory=${MEMORY} --cpu=${CPU}

else # if build fails, then exit
    echo "--------------------------------------------------------------------------------"
    echo "Build failed. Exiting ..."
    echo "--------------------------------------------------------------------------------"
    exit 1
fi


echo "--------------------------------------------------------------------------------"
echo "Done."