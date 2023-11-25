#!/bin/bash
# Usage: ./RUN -r (restart)

# Replace with the name of your Python script
DIR="$( cd -- "$( dirname -- "${BASH_SOURCE[0]:-$0}"; )" &> /dev/null && pwd 2> /dev/null; )";
SCRIPT_NAME=`basename "$0"` # with extension
NAME="${SCRIPT_NAME%.*}" # no extension
APP_NAME="$DIR/app.py"
PROJECT="$(basename "${DIR}")" # parent dir name
LOG="${DIR}/logs/${PROJECT}.log"
PYTHON="/usr/bin/python"
REQUIRES_SUDO=false
mkdir -p "$(dirname "$LOG")"

# Use getopts to parse the --restart option
while getopts "r" opt; do
  case $opt in
    r) # Set a flag to indicate the --restart option is given
       RESTART=1;;
    *) # Print an error message for invalid options
       echo "Invalid option: -$OPTARG" >&2
       exit 1;;
  esac
done

# Check if the script is run with sudo
if [ "$EUID" -ne 0 ] && $REQUIRES_SUDO; then
  # If not, re-run the script with sudo and pass the original arguments
  echo "Re-running this script with sudo."
  sudo "$0" "$@"
  exit $?
fi

cd $DIR

if pgrep -f "$APP_NAME" >/dev/null; then
  echo "$APP_NAME is already running"
  # Check if the --restart option is given
  if [ "$RESTART" == "1" ]; then
    # Kill any running app.py processes
    echo "Killing if already running"
    pkill -f $APP_NAME
    sleep 2
    $PYTHON $APP_NAME > "$LOG" 2>&1 &

  fi

else
  echo "$APP_NAME is not running. Starting it now..."
  # Replace with the command to start your Python script
  $PYTHON $APP_NAME > "$LOG" 2>&1 &
fi
