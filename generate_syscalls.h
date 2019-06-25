#!/bin/bash

curl https://raw.githubusercontent.com/NetBSD/src/trunk/sys/sys/syscall.h > syscall.h
cat syscall.h | grep "SYS_" | awk -F'SYS_' '{ print $2 }' | sed -nE 's|([^A-Z][a-zA-Z0-9_]+)\t(.*)|\2:"\1"|p' > syscalls.dict 
