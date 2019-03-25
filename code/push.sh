#!/bin/bash
# Pushes code from my laptop to the RPi

source ./constants.conf

# Push new code and then run the new code if no arguments are given
if [ $# -le 0 ]
then 
	echo -e "\nPushing Code to $external_ip\n"
	scp -r ../code $external_host_name@$external_ip:$path_to_push_to

	echo -e "\nRunning Code on $external_ip\n"
	ssh -t $external_host_name@$external_ip 'cd /home/ilite/Mission_Control_2019_files/code;
						export DISPLAY=:0;
						./start_command_console.sh'

# Else, (arguments are given) go through the options loop
else
	while getopts ":prm" opt; do
		case ${opt} in
			p ) 
				echo -e "\nPushing Code to $external_ip\n"
				scp -r ../code $external_host_name@$external_ip:$path_to_push_to
				;;
			r ) 
				echo -e "\nRunning Code on $external_ip\n"
				ssh -t $external_host_name@$external_ip 'cd /home/ilite/Mission_Control_2019_files/code;
											export DISPLAY=:0;
											./start_command_console.sh'
				;;
			m ) 
				echo -e "\nPushing Media to $external_ip\n"
				scp -r ../media $external_host_name@$external_ip:$path_to_push_to
				;;
			\? )
				echo "Usage push.sh [-?]"
				echo "-p for pushing CODE without running anything"
				echo "-r to run the code currently on the pi"
				echo "-m to push the MEDIA folder to the pi"
				echo "		this is the only way to push new media"
				echo "Running without arguments will push code and then run"
				;;
		esac
	done
fi