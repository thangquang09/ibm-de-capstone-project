#!/bin/bash

# Variables
DB_HOST="mysql"          # Database host (use container name)
DB_USER="root"               # Database user
DB_PASSWORD="mysecretpassword" # Database password
DB_NAME="sales"             # Database name
TABLE_NAME="sales_data"      # Table to export
OUTPUT_FILE="sales_data.sql" # Output file name

# Export the data from sales_data table to an SQL script
mysqldump -h $DB_HOST -u $DB_USER -p$DB_PASSWORD $DB_NAME $TABLE_NAME > $OUTPUT_FILE

# Check if the command was successful
if [ $? -eq 0 ]; then
    echo "Data exported successfully to $OUTPUT_FILE"
else
    echo "Failed to export data from $TABLE_NAME"
fi
