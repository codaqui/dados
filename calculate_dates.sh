# Author: Enderson Menezes
# Usage: bash calculate_dates.sh <arg>
# Valid args:
# - last_month
# - MMYYYY
# Return = DD-MM-YYYY DD-MM-YYYY

ARGUMENT=$1
## Argument = MMYYYY
if [[ $ARGUMENT =~ ^[0-9]{6}$ ]]; then
    # Extract month and year from MMYYYY format
    MONTH=${ARGUMENT:0:2}
    YEAR=${ARGUMENT:2:4}
    FIRST_DAY_MONTH=$(date -d "$YEAR-$MONTH-01" +%Y-%m-%d)
    LAST_DAY_MONTH=$(date -d "$FIRST_DAY_MONTH +1 month -1 day" +%Y-%m-%d)
## Argument = last_month OR $GITHUB_EVENT_NAME = schedule
elif [[ $ARGUMENT == "last_month" || $GITHUB_EVENT_NAME == "schedule" ]]; then
    FIRST_DAY_MONTH=$(date -d "$(date +%Y)-$(date +%m)-01 -1 month" +%Y-%m-%d)
    LAST_DAY_MONTH=$(date -d "$FIRST_DAY_MONTH +1 month -1 day" +%Y-%m-%d)
else
    echo "Invalid argument. Please use 'last_month' or MMYYYY format (e.g., 012025)"
    exit 1
fi
FIRST_DAY_MONTH=$(date -d $FIRST_DAY_MONTH +%d-%m-%Y)
LAST_DAY_MONTH=$(date -d $LAST_DAY_MONTH +%d-%m-%Y)
echo $FIRST_DAY_MONTH $LAST_DAY_MONTH
