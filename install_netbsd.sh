#!/bin/sh

usage()
{
	echo "USAGE : $0 [OPTIONS]"
	echo "Options :  "
	echo "	-s : Download and setup anita"
	echo "	-i : install a NetBSD image"
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
			pip install --upgrade pexpect
			git clone https://github.com/gson1703/anita.git anita/
			
			# Modifications neccesary on Ubuntu 
			sed -e 's_#!/usr/pkg/bin/python2.4_#!/usr/bin/python_' anita/anita > temp_anita
			mv temp_anita anita/anita
			rm temp_anita
			chmod +x anita/anita
			;;
		i)
			echo "Installing a NetBSD image"
			# Output directory
			mkdir out/

			# Install from release tree
			./anita/anita --workdir=./ install http://nycdn.netbsd.org/pub/NetBSD-daily/HEAD/latest/amd64/

			# Setup ssh keys
			ssh-keygen -t rsa -f key -N ""
			SSHKEY=$(cat key.pub)

			# Setup ssh
			./anita/anita --run="\
echo -e 'dhcpcd=YES\nsshd=YES' >> /etc/rc.conf; \
mkdir .ssh; \
echo $SSHKEY > .ssh/authorized_keys;  \
sed -e 's/^#PermitRootLogin [a-z][a-z-]*$/PermitRootLogin yes/' /etc/ssh/sshd_config > sshd_config; \
mv sshd_config /etc/ssh/sshd_config; \
poweroff; \
			" --persist --no-install --workdir=./ interact http://nycdn.netbsd.org/pub/NetBSD-daily/HEAD/latest/amd64/

			# Copy image key pair
			mv key* out/
			mv wd0.img out/netbsd.img

			# Clean current dir
			rm -rf download
			;;
		*)
			echo "Invalid Option "
            		usage
            		;;
	esac
done
