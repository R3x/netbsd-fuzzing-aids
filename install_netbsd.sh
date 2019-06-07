#!/bin/sh

usage()
{
	echo "USAGE : $0 [OPTIONS]"
	echo "Options :  "
	echo "	-s : Download and setup anita"
	echo "	-i : install a NetBSD image"
	echo "	-p : Patch Anita(if -i doesn't work)"
}

if [ $# -eq 0 ]
then
    usage
    exit
fi

while getopts "si" opt
do
	case "${opt}" in
		s)
			echo "Setting up Anita"
			# clearing previous output
			rm -rf anita/

			# APT - installs that might be needed
			#sudo apt-get install genisoimage
			#sudo apt-get install python-pip

			pip2.7 install --upgrade pexpect
			git clone https://github.com/gson1703/anita.git anita/
			
			# Modifications neccesary on Ubuntu 
			sed -i -e 's_#!/usr/pkg/bin/python2.4_#!/usr/bin/python_' anita/anita 
			
			;;
		i)
			echo "Installing a NetBSD image"
			# removing previous stuff
			rm -rf out
			
			# Output directory
			mkdir out/

			# Install from release tree
			./anita/anita --workdir=./ --disk-size=2G --memory-size=1024M install http://nycdn.netbsd.org/pub/NetBSD-daily/HEAD/latest/amd64/

			# Setup ssh keys
			ssh-keygen -t rsa -f key -N ""
			SSHKEY=$(cat key.pub)

			# Setup ssh
			./anita/anita --run="\
echo -e 'dhcpcd=YES\nsshd=YES\npostfix=NO\ncron=NO\nmakemandb=NO\ncgd=NO\ninetd=NO' >> /etc/rc.conf; \
touch /fastboot; \
mkdir .ssh; \
echo $SSHKEY > .ssh/authorized_keys;  \
sed -i -e 's/^#PermitRootLogin [a-z][a-z-]*$/PermitRootLogin yes/' /etc/ssh/sshd_config; \
sed -i -e 's/^ddb.onpanic?=0/ddb.onpanic=1/' /etc/sysctl.conf; \
echo -e 'ddb.commandonenter=\"show panic;bt;show registers;ps;show all locks;show all pages;show all pools\"\nddb.lines=0\nddb.maxwidth=0' >> /etc/sysctl.conf; \
cd /dev; \
./MAKEDEV kcov; \
poweroff; \
			" --persist --no-install --workdir=./ interact http://nycdn.netbsd.org/pub/NetBSD-daily/HEAD/latest/amd64/

			# Copy image key pair
			mv key* out/
			mv wd0.img out/image

			# Clean current dir
			rm -rf download
			;;
		p)
			echo "Applying patches to anita"
			line=$(($(grep -nr "\"cdrom\", bootcd" anita/anita.py | awk -F ":" '{print $1}') + 1))
			sed -i "$line s/True/False" anita/anita.py 
			;;
		*)
			echo "Invalid Option "
            		usage
            		;;
	esac
done
