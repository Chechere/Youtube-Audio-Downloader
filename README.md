# Youtube-Audio-Downloader
Project for an android app that downloads audio from youtube videos.


## Download branch

    git clone --branch android https://github.com/Chechere/Youtube-Audio-Downloader.git

## Create Virtualenv

    virtualenv .kivy

Make sure virtualenv is installed: 

    sudo apt install python3-venv

## Open Virtualenv
    -Linux: source .kivy/bin/activate
    -Windows: .kivy/scripts/activate.bat

## Install Buildozer

Used to build project apk.

    pip3 install --user --upgrade buildozer

    sudo apt update

    sudo apt install -y git zip unzip openjdk-17-jdk python3-pip autoconf libtool pkg-config zlib1g-dev libncurses5-dev libncursesw5-dev libtinfo5 cmake libffi-dev libssl-dev

    #This must be done on the virtualenv
    pip3 install --upgrade Cython==0.29.33 virtualenv

    export PATH=$PATH:~/.local/bin/

## Install Requirements
    pip install -r requirements.txt



## Deployment

To deploy this project run (With virtualenv activated)
    
    buildozer -v android debug

## WSL moving apk to Windows
    sudo mv bin/<APK FILE NAME> /mnt/c/<DIR FOLDER>
Optional: apk name can be changed on move

    sudo mv bin/<APK FILE NAME> /mnt/c/<DIR FOLDER>/<NEW NAME>.apk
Recommendation: For easy use move it to a folder inside de drive directory

    sudo mv bin/<APK FILE NAME> /mnt/c/UbuntuShared
    sudo mv bin/<APK FILE NAME> /mnt/c/UbuntuShared/<NEW NAME>.apk
This is an example with a folder in directory C:/UbuntuShared


