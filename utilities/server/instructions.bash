# step 1
cd ~

# step 2
if [ ! -d "clean-smrs" ]; then
    echo "Cloning the repository..."
    git clone https://github.com/cookii-king/clean-smrs.git
fi

# step 3
sudo chmod +x /home/ubuntu/clean-smrs/utilities/server/setup.bash
sudo bash /home/ubuntu/clean-smrs/utilities/server/setup.bash