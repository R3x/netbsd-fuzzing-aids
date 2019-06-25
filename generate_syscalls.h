#!/bin/bash

SRC_ROOT=
cat $SRC_ROOT/sys/sys/syscall.h | grep "SYS_" | awk -F'SYS_' '{ print $2 }' | sed -nE 's|([^A-Z][a-zA-Z0-9_]+)\t(.*)|\2:"\1"|p' 
