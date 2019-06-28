import re
import sys
import os

def usage():
    print "USAGE: python modify_header.py <headerfile> <struct name>"

typedef_stored = {}

def main():
    struct_finder = re.compile("typedef struct \{([^}]*?)\} (.*);")
    typedef_finder = re.compile("typedef[ \t](.*)[ \t](.*?)[\[;]")
    member_finder = re.compile("[^t\n]*?[ \t](.*)[ \t](.*);")
    if len(sys.argv) < 2:
        usage()
        exit()
    fp = open(sys.argv[1])
    content = fp.read()
    fp.close()
    wfp = open("temp.h", "w+")
    rfp = open("temp2.h", "w+")
    structs = struct_finder.findall(content)
    typedefs = typedef_finder.findall(content)
    for typedef in typedefs:
        typedef_stored[typedef[1].strip().strip('\t')] = typedef[0].strip().strip('\t')
    print typedef_stored
    wfp.write(content)
    for struct in structs:
        print "structs found " + struct[1]
        if cmp(struct[1], sys.argv[2]) != 0:
            continue
        wfp.write("\ntypedef struct  " + struct[1] + "\t_" + struct[1] + ";") 
        wfp.write("\nstruct " + struct[1] + "{" + struct[0] + "};")
    wfp.seek(0)
    content = wfp.readlines()
    content2 = []
    content3 = []
    for line in content:
        match = member_finder.match(line)
        if match:
            if typedef_stored.has_key(match.groups()[0].strip().strip('\t')):
                line = line.replace(match.groups()[0].strip().strip('\t'), typedef_stored[match.groups()[0].strip().strip('\t')])
                print line
        content2.append(line)
    for line in content2:
        match = member_finder.match(line)
        if match:
            if typedef_stored.has_key(match.groups()[0].strip().strip('\t')):
                line = line.replace(match.groups()[0].strip().strip('\t'), typedef_stored[match.groups()[0].strip().strip('\t')])
                print line
        content3.append(line)
    rfp.writelines(content3)
    wfp.close()
    rfp.close()
    #os.rename("temp.h", sys.argv[1])
    os.rename("temp2.h", sys.argv[1])

if __name__ == "__main__":
    main()
