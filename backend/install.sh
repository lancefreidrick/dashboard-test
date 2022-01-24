#!/bin/bash

BOLD=$(tput bold)
NORM=$(tput sgr0)

title-echo () {
	echo -e "${BOLD}\033[1;32m==>\033[0m ${BOLD}${1}...${NORM}"
}

subtitle-echo () {
	echo -e "  ${BOLD}\033[1;36m->\033[0m ${1}${NORM}"
}

error-echo () {
	echo -e "${BOLD}\033[1;31m==> ERROR:\033[0m ${BOLD}${1}${NORM}"
}

REQUIRED_ENV_VARIABLES=(
	'MONGODB_HOST'
	'MONGODB_PORT'
	'PG_CONNECTION_STRING'
	'SENDGRID_SECRET_KEY'
	'SENDGRID_MODE'
	'SENDGRID_SENDER'
	'AWS_S3_ACCESS_KEY'
	'AWS_S3_SECRET_KEY'
	'AWS_S3_BUCKET_NAME'
	'AWS_S3_REGION'
)

# Checks if Python is installed
title-echo 'Checking Python installation'
[[ ! "$(command -v python)" && ! "$(command -v python3)" ]] && error-echo 'No Python installed' && exit 1

VERSION_ERROR=1
ACCEPTED_VERSIONS='3\.(6|7)'

# Checks if Python version is valid. Current repo uses 3.(6|7).x. Works for both python and python3
[ "$(command -v python3)" ] && python3 --version 2>&1 | egrep -q "$ACCEPTED_VERSIONS" && VERSION_ERROR=0 && PYTHON_CMD=python3 && subtitle-echo "Using command 'python3'"
[[ "$VERSION_ERROR" == 1 && "$(command -v python)" ]] && python --version 2>&1 | egrep -q "$ACCEPTED_VERSIONS" && VERSION_ERROR=0 && PYTHON_CMD=python && subtitle-echo "Using command 'python'"

[ "$VERSION_ERROR" == 1 ] && error-echo "Python version mismatch (Needs 3.6.x or 3.7.x)" && exit 2
subtitle-echo "Python version is satisfied ($($PYTHON_CMD --version 2>&1))"

# Check if PostgreSQL is installed
title-echo 'Checking PostgreSQL installation'
[ ! "$(command -v psql)" ] && error-echo 'No installation' && exit 3
subtitle-echo 'Installation detected'

# Check if PostgreSQL instance is running
[ "$(pg_isready > /dev/null 2>&1)" ] && error-echo 'Instance not running' && exit 4
subtitle-echo 'Instance running'

# Check if MongoDB is installed
title-echo 'Checking MongoDB installation'
[ ! "$(command -v mongo)" ] && error-echo 'No installation' && exit 5
subtitle-echo 'Installation detected'

# Check if MongoDB instance is running
[ "$(systemctl status mongod.service > /dev/null 2>&1)" ] && error-echo 'Instance not running' && exit 6
subtitle-echo 'Instance running'

# Asks for environment file
title-echo 'Checking environment file'
ENV_PATH=$(pwd)/.env

# Checks if given env path exists
[ ! -f "$ENV_PATH" ] && error-echo 'Environment file does not exist' && exit 7
subtitle-echo 'Environment file found'

# Check if environment file contains necessary variables
title-echo 'Checking required environment variables'
HAS_ERROR=0

for ITEM in "${REQUIRED_ENV_VARIABLES[@]}"; do
	[ "$(awk -F '=' "/^$ITEM/ {print \$2}" "$ENV_PATH" | wc -w)" == 0 ] && error-echo "No value for $ITEM provided (required)" && HAS_ERROR=1
done

[ $HAS_ERROR == 1 ] && error-echo 'Required environment variables must be populated before proceeding' && exit 8
subtitle-echo 'All required variables populated'

# Check if venv exists
title-echo 'Checking Python virtual environment'

# Check if venv package is installed
$PYTHON_CMD -c 'import venv' > /dev/null 2>&1
[ $? != 0 ] && error-echo "Python 'venv' utility is not installed" && exit 9
subtitle-echo "Python 'venv' utility is installed"

[ -d ./venv ] && rm -rf ./venv && subtitle-echo 'Removing old virtual environment'

# Create Python virtual environment
$PYTHON_CMD -m venv venv && subtitle-echo 'Created new virtual environment'

# Use Python virtual environment
title-echo 'Going into virtual environment'
source ./venv/bin/activate

# Update pip to most recent version
subtitle-echo 'Upgrading pip'
$PYTHON_CMD -m pip install --upgrade pip > /dev/null 2>&1
subtitle-echo 'pip has been upgraded to the latest version'

# Install required packages
title-echo 'Installing required packages'
pip install -r requirements.txt

# Exit Python virtual environment
title-echo 'Exiting virtual environment'
deactivate
