#!/bin/bash

# Path to the root folder containing the ticker folders
root_folder="/Users/amirk.khandani/Documents/scraper"

# Azure storage account name
account_name="earningtranscripts"

# Iterate over each ticker folder
for ticker_folder in "$root_folder"/*; do
    # Check if the item is a folder
    if [ -d "$ticker_folder" ]; then
        # Extract the ticker name from the folder path
        ticker=$(basename "$ticker_folder")
        new_ticker=$(echo "$ticker" | tr '[:upper:]' '[:lower:]')"-ticker"
        
        # Iterate over each subfolder within the ticker folder
        for subfolder in "$ticker_folder"/*; do
            # Check if the item is a folder
            if [ -d "$subfolder" ]; then
                # Extract the subfolder name from the path
                subfolder_name=$(basename "$subfolder")
                
                # Iterate over each file in the subfolder
                for file_path in "$subfolder"/*; do
                    # Check if the item is a file and does not end with ".txt"
                    if [ -f "$file_path" ] && [[ ! "$file_path" =~ \.txt$ ]]; then
                        # Extract the file name from the path
                        file_name=$(basename "$file_path")
                        
                        # Upload the file to the respective Azure container
                        az storage blob upload \
                            --account-name "$account_name" \
                            --container-name "$new_ticker" \
                            --name "$subfolder_name/$file_name" \
                            --type block \
                            --file "$file_path" \
                            --auth-mode login
                        
                        echo "Uploaded $file_name to $ticker/$subfolder_name"
                    fi
                done
            fi
        done
    fi
done