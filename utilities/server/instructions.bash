#!/bin/bash

# Step 1: Navigate to the home directory
cd ~

# Step 2: Clone the repository if not already cloned
if [ ! -d "clean-smrs" ]; then
    echo "Cloning the repository..."
    git clone https://github.com/cookii-king/clean-smrs.git
fi

# Step 3: Ask the user to choose between Django and Flask
echo "Choose the application to configure:"
echo "1) Django"
echo "2) Flask"
read -p "Enter the number of your choice: " choice

# Validate the input
if [[ "$choice" =~ ^[1-2]$ ]]; then
    # Pass the choice as an argument to setup.bash
    sudo chmod +x /home/ubuntu/clean-smrs/utilities/server/setup.bash
    sudo bash /home/ubuntu/clean-smrs/utilities/server/setup.bash "$choice"
else
    echo "Invalid choice. Please run the script again and select either 1 or 2."
    exit 1
fi