import re
import sys
import os

def usage():
    print "USAGE: python modify_header.py <headerfile>"

def main():
    struct_finder = re.compile("typedef struct \{([^}]*?)\} (.*);")
    if len(sys.argv) < 2:
        usage()
        exit()
    fp = open(sys.argv[1])
    content = fp.read()
    fp.close()
    wfp = open("temp.h", "w+")
    wfp.write(content)
    structs = struct_finder.findall(content)
    for struct in structs:
        print "structs found " + struct[1]
        wfp.write("\ntypedef struct  _" + struct[1] + "\t" + struct[1]) 
        wfp.write("\nstruct " + struct[1] + "{" + struct[0] + "};")
    #os.rename("temp.h", sys.argv[1])

if __name__ == "__main__":
    main()
