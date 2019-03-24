#!/bin/bash

output_ip=$(<external_ip)
username=ilite

if [ "$1" == "-p" ]
then
	echo -e "\nPushing Code to $output_ip\n"
	scp -r ../code $username@$output_ip:/home/ilite/Mission_Control_2019_files

elif [  "$1" == "-r"  ]
then
	echo -e "\nRunning Code on $output_ip\n"
	ssh -t $username@$output_ip 'cd Desktop/videos/code;
						export DISPLAY=:0;
						./start_command_console.sh'
else
	echo -e "\nPushing Code to $output_ip\n"
	scp -r ../code $username@$output_ip:/home/ilite/Mission_Control_2019_files

	echo -e "\nRunning Code on $output_ip\n"
	ssh -t $username@$output_ip 'cd Desktop/videos/code;
						export DISPLAY=:0;
						./start_command_console.sh'
fi

# I may need to add this > "chmod +x start_command_console.sh;" back in
# I didn't add bin/bash to the front of the file originally which is why
# I was having to do it on the RPi