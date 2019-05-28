# netbsd-fuzzing-aids

This repository contains scripts that may be useful for fuzzing the NetBSD kernel.

## Automatic Image creation 

Fuzzing NetBSD requires images to be created from NetBSD-HEAD often. Currently we use
[anita](http://gson.org/netbsd/anita/) to create images.

The image created comes with an ssh key which can be used to log in as root.

### Instructions

The script is written with the assumption of a Linux environment.

`
./install_netbsd.sh -s
./install_netbsd.sh -i
`

After the installation is complete you can find a `netbsd.img` and `key` file in the
`out/` directory. You can now use the image to boot a NetBSD kernel.

