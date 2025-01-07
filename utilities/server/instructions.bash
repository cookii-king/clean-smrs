#!/bin/bash

# Step 1: Navigate to the home directory
cd ~

# Step 2: Clone the repository if not already cloned
if [ ! -d "clean-smrs" ]; then
    echo "Cloning the repository..."
    git clone https://github.com/cookii-king/clean-smrs.git
fi