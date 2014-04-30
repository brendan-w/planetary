#!/bin/bash

# Check if an external device exists
if [ -e /run/media/$USER/* ]; then

    # Build the .xo file
    echo 'Found external device.'
    echo 'Building xo file...'
    ./setup.py dist_xo
    file=dist/*.xo
    $(echo $file | cut -f1 -d-)

    # Check if the file already exists
    if [ -e /run/media/$USER/*/$file ]; then
echo 'Removing version on device...'
        rm /run/media/$USER/*/$file
    fi

    # Move the new file onto the external device
    echo 'Moving xo file to device...'
    mv $file /run/media/$USER/*/
    echo 'Cleaning up...'
    rm -r dist/

# Notify the user a device was not found
else
echo 'No external device found.'
    echo 'Building xo file...'
    ./setup.py dist_xo
    file=dist/*.xo
    activity=$(echo $(echo $file | cut -f1 -d-) | cut -f2 -d/)

    # Check if there is a current version of the xo file in your directory
    if [ -e ./$activity-*.xo ]; then
        # Prompt the user if they would like to replace the file or not
        echo -n 'Would you like to replace the current xo file? [y/n]: '
        read answer

        # If the user wants to replace the file, replace it
        if [ "$answer" == "y" ]; then
echo 'Removing previous version...'
            rm ./$activity-*.xo
            mv dist/* ./
            
        # If the user does not want to replace the file,
        # save the old one and create the new file
        elif [ "$answer" == "n" ]; then
old=$activity-*.xo
            mv ./$old ./$activity.old.xo
            mv ./$file ./$activity.new.xo

        else
echo 'Invalid input.'
            echo 'Aborting.'
            rm -r dist/
            exit 1
        fi
else
mv dist/* ./
    fi

echo 'Cleaning up...'
    rm -r dist/
fi

echo 'Finished!'