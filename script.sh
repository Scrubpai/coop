#!/bin/bash

# Path to the root folder containing the subfolders
root_folder="/Users/amirk.khandani/Documents/scraper"

# Azure storage account name
account_name="earningtranscripts"

# Iterate over each subfolder in the root folder
for folder_name in "$root_folder"/*; do
    # Check if the item is a folder
    if [ -d "$folder_name" ]; then
        # Extract the folder name from the path
        folder_name=$(basename "$folder_name")
        new_folder_name=$(echo "$folder_name" | tr '[:upper:]' '[:lower:]')"-ticker"

        # echo "Folder Name: $folder_name"

        # Create the Azure container using the az command
        az storage container create \
            --account-name "$account_name" \
            --name "$new_folder_name" \
            --auth-mode login
    fi
done