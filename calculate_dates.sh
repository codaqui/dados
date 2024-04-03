# Author: Enderson Menezes
# Usage: bash calculate_dates.sh ARG1
# Arg1 = last_month or integer 01 --> 12
# Return = DD-MM-YYYY DD-MM-YYYY

ARGUMENT=$1
if [[ $ARGUMENT =~ ^[0-9]{2}$ ]]; then
    FIRST_DAY_MONTH=$(date -d "$(date +%Y)-$ARGUMENT-01" +%Y-%m-%d)
    LAST_DAY_MONTH=$(date -d "$FIRST_DAY_MONTH +1 month -1 day" +%Y-%m-%d)
elif [[ $ARGUMENT == "last_month" ]]; then
    FIRST_DAY_MONTH=$(date -d "$(date +%Y)-$(date +%m)-01 -1 month" +%Y-%m-%d)
    LAST_DAY_MONTH=$(date -d "$FIRST_DAY_MONTH +1 month -1 day" +%Y-%m-%d)
else
    echo "Invalid argument. Please use last_month or integer 01 --> 12"
    exit 1
fi
FIRST_DAY_MONTH=$(date -d $FIRST_DAY_MONTH +%d-%m-%Y)
LAST_DAY_MONTH=$(date -d $LAST_DAY_MONTH +%d-%m-%Y)
echo $FIRST_DAY_MONTH $LAST_DAY_MONTH
