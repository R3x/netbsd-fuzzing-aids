import re
import sys
import os

syzcalls = {0:"syscall",1:"exit",2:"fork",3:"read",4:"write",5:"open",6:"close",7:"compat_50_wait4",8:"compat_43_ocreat",9:"link",10:"unlink",12:"chdir",13:"fchdir",14:"compat_50_mknod",15:"chmod",16:"chown",17:"break",18:"compat_20_getfsstat",19:"compat_43_olseek",20:"getpid",21:"compat_40_mount",22:"unmount",23:"setuid",24:"getuid",25:"geteuid",26:"ptrace",27:"recvmsg",28:"sendmsg",29:"recvfrom",30:"accept",31:"getpeername",32:"getsockname",33:"access",34:"chflags",35:"fchflags",36:"sync",37:"kill",38:"compat_43_stat43",39:"getppid",40:"compat_43_lstat43",41:"dup",42:"pipe",43:"getegid",44:"profil",45:"ktrace",46:"compat_13_sigaction13",47:"getgid",48:"compat_13_sigprocmask13",49:"__getlogin",50:"__setlogin",51:"acct",52:"compat_13_sigpending13",53:"compat_13_sigaltstack13",54:"ioctl",55:"compat_12_oreboot",56:"revoke",57:"symlink",58:"readlink",59:"execve",60:"umask",61:"chroot",62:"compat_43_fstat43",63:"compat_43_ogetkerninfo",64:"compat_43_ogetpagesize",65:"compat_12_msync",66:"vfork",71:"compat_43_ommap",72:"vadvise",73:"munmap",74:"mprotect",75:"madvise",78:"mincore",79:"getgroups",80:"setgroups",81:"getpgrp",82:"setpgid",83:"compat_50_setitimer",84:"compat_43_owait",85:"compat_12_oswapon",86:"compat_50_getitimer",87:"compat_43_ogethostname",88:"compat_43_osethostname",89:"compat_43_ogetdtablesize",90:"dup2",92:"fcntl",93:"compat_50_select",95:"fsync",96:"setpriority",97:"compat_30_socket",98:"connect",99:"compat_43_oaccept",100:"getpriority",101:"compat_43_osend",102:"compat_43_orecv",103:"compat_13_sigreturn13",104:"bind",105:"setsockopt",106:"listen",108:"compat_43_osigvec",109:"compat_43_osigblock",110:"compat_43_osigsetmask",111:"compat_13_sigsuspend13",112:"compat_43_osigstack",113:"compat_43_orecvmsg",114:"compat_43_osendmsg",116:"compat_50_gettimeofday",117:"compat_50_getrusage",118:"getsockopt",120:"readv",121:"writev",122:"compat_50_settimeofday",123:"fchown",124:"fchmod",125:"compat_43_orecvfrom",126:"setreuid",127:"setregid",128:"rename",129:"compat_43_otruncate",130:"compat_43_oftruncate",131:"flock",132:"mkfifo",133:"sendto",134:"shutdown",135:"socketpair",136:"mkdir",137:"rmdir",138:"compat_50_utimes",140:"compat_50_adjtime",141:"compat_43_ogetpeername",142:"compat_43_ogethostid",143:"compat_43_osethostid",144:"compat_43_ogetrlimit",145:"compat_43_osetrlimit",146:"compat_43_okillpg",147:"setsid",148:"compat_50_quotactl",149:"compat_43_oquota",150:"compat_43_ogetsockname",155:"nfssvc",156:"compat_43_ogetdirentries",157:"compat_20_statfs",158:"compat_20_fstatfs",161:"compat_30_getfh",162:"compat_09_ogetdomainname",163:"compat_09_osetdomainname",164:"compat_09_ouname",165:"sysarch",169:"compat_10_osemsys",170:"compat_10_omsgsys",171:"compat_10_oshmsys",173:"pread",174:"pwrite",175:"compat_30_ntp_gettime",176:"ntp_adjtime",181:"setgid",182:"setegid",183:"seteuid",184:"lfs_bmapv",185:"lfs_markv",186:"lfs_segclean",187:"compat_50_lfs_segwait",188:"compat_12_stat12",189:"compat_12_fstat12",190:"compat_12_lstat12",191:"pathconf",192:"fpathconf",193:"getsockopt2",194:"getrlimit",195:"setrlimit",196:"compat_12_getdirentries",197:"mmap",198:"__syscall",199:"lseek",200:"truncate",201:"ftruncate",202:"__sysctl",203:"mlock",204:"munlock",205:"undelete",206:"compat_50_futimes",207:"getpgid",208:"reboot",209:"poll",210:"afssys",220:"compat_14___semctl",221:"semget",222:"semop",223:"semconfig",224:"compat_14_msgctl",225:"msgget",226:"msgsnd",227:"msgrcv",228:"shmat",229:"compat_14_shmctl",230:"shmdt",231:"shmget",232:"compat_50_clock_gettime",233:"compat_50_clock_settime",234:"compat_50_clock_getres",235:"timer_create",236:"timer_delete",237:"compat_50_timer_settime",238:"compat_50_timer_gettime",239:"timer_getoverrun",240:"compat_50_nanosleep",241:"fdatasync",242:"mlockall",243:"munlockall",244:"compat_50___sigtimedwait",245:"sigqueueinfo",246:"modctl",247:"_ksem_init",248:"_ksem_open",249:"_ksem_unlink",250:"_ksem_close",251:"_ksem_post",252:"_ksem_wait",253:"_ksem_trywait",254:"_ksem_getvalue",255:"_ksem_destroy",256:"_ksem_timedwait",257:"mq_open",258:"mq_close",259:"mq_unlink",260:"mq_getattr",261:"mq_setattr",262:"mq_notify",263:"mq_send",264:"mq_receive",265:"compat_50_mq_timedsend",266:"compat_50_mq_timedreceive",270:"__posix_rename",271:"swapctl",272:"compat_30_getdents",273:"minherit",274:"lchmod",275:"lchown",276:"compat_50_lutimes",277:"__msync13",278:"compat_30___stat13",279:"compat_30___fstat13",280:"compat_30___lstat13",281:"__sigaltstack14",282:"__vfork14",283:"__posix_chown",284:"__posix_fchown",285:"__posix_lchown",286:"getsid",287:"__clone",288:"fktrace",289:"preadv",290:"pwritev",291:"compat_16___sigaction14",292:"__sigpending14",293:"__sigprocmask14",294:"__sigsuspend14",295:"compat_16___sigreturn14",296:"__getcwd",297:"fchroot",298:"compat_30_fhopen",299:"compat_30_fhstat",300:"compat_20_fhstatfs",301:"compat_50_____semctl13",302:"compat_50___msgctl13",303:"compat_50___shmctl13",304:"lchflags",305:"issetugid",306:"utrace",307:"getcontext",308:"setcontext",309:"_lwp_create",310:"_lwp_exit",311:"_lwp_self",312:"_lwp_wait",313:"_lwp_suspend",314:"_lwp_continue",315:"_lwp_wakeup",316:"_lwp_getprivate",317:"_lwp_setprivate",318:"_lwp_kill",319:"_lwp_detach",320:"compat_50__lwp_park",321:"_lwp_unpark",322:"_lwp_unpark_all",323:"_lwp_setname",324:"_lwp_getname",325:"_lwp_ctl",330:"compat_60_sa_register",331:"compat_60_sa_stacks",332:"compat_60_sa_enable",333:"compat_60_sa_setconcurrency",334:"compat_60_sa_yield",335:"compat_60_sa_preempt",340:"__sigaction_sigtramp",343:"rasctl",344:"kqueue",345:"compat_50_kevent",346:"_sched_setparam",347:"_sched_getparam",348:"_sched_setaffinity",349:"_sched_getaffinity",350:"sched_yield",351:"_sched_protect",354:"fsync_range",355:"uuidgen",356:"getvfsstat",357:"statvfs1",358:"fstatvfs1",359:"compat_30_fhstatvfs1",360:"extattrctl",361:"extattr_set_file",362:"extattr_get_file",363:"extattr_delete_file",364:"extattr_set_fd",365:"extattr_get_fd",366:"extattr_delete_fd",367:"extattr_set_link",368:"extattr_get_link",369:"extattr_delete_link",370:"extattr_list_fd",371:"extattr_list_file",372:"extattr_list_link",373:"compat_50_pselect",374:"compat_50_pollts",375:"setxattr",376:"lsetxattr",377:"fsetxattr",378:"getxattr",379:"lgetxattr",380:"fgetxattr",381:"listxattr",382:"llistxattr",383:"flistxattr",384:"removexattr",385:"lremovexattr",386:"fremovexattr",387:"compat_50___stat30",388:"compat_50___fstat30",389:"compat_50___lstat30",390:"__getdents30",392:"compat_30___fhstat30",393:"compat_50___ntp_gettime30",394:"__socket30",395:"__getfh30",396:"__fhopen40",397:"__fhstatvfs140",398:"compat_50___fhstat40",399:"aio_cancel",400:"aio_error",401:"aio_fsync",402:"aio_read",403:"aio_return",404:"compat_50_aio_suspend",405:"aio_write",406:"lio_listio",410:"__mount50",411:"mremap",412:"pset_create",413:"pset_destroy",414:"pset_assign",415:"_pset_bind",416:"__posix_fadvise50",417:"__select50",418:"__gettimeofday50",419:"__settimeofday50",420:"__utimes50",421:"__adjtime50",422:"__lfs_segwait50",423:"__futimes50",424:"__lutimes50",425:"__setitimer50",426:"__getitimer50",427:"__clock_gettime50",428:"__clock_settime50",429:"__clock_getres50",430:"__nanosleep50",431:"____sigtimedwait50",432:"__mq_timedsend50",433:"__mq_timedreceive50",434:"compat_60__lwp_park",435:"__kevent50",436:"__pselect50",437:"__pollts50",438:"__aio_suspend50",439:"__stat50",440:"__fstat50",441:"__lstat50",442:"____semctl50",443:"__shmctl50",444:"__msgctl50",445:"__getrusage50",446:"__timer_settime50",447:"__timer_gettime50",448:"__ntp_gettime50",449:"__wait450",450:"__mknod50",451:"__fhstat50",453:"pipe2",454:"dup3",455:"kqueue1",456:"paccept",457:"linkat",458:"renameat",459:"mkfifoat",460:"mknodat",461:"mkdirat",462:"faccessat",463:"fchmodat",464:"fchownat",465:"fexecve",466:"fstatat",467:"utimensat",468:"openat",469:"readlinkat",470:"symlinkat",471:"unlinkat",472:"futimens",473:"__quotactl",474:"posix_spawn",475:"recvmmsg",476:"sendmmsg",477:"clock_nanosleep",478:"___lwp_park60",479:"posix_fallocate",480:"fdiscard",481:"wait6",482:"clock_getcpuclockid2"}
    
def sanity_check():
    obsolete=[]
    ctr = 0
    for i, j in syzcalls.items():
        if i != ctr:
            print str(i) + "  :  " + j
            print "missing syscall at " + str(ctr) + " : " + str(i)
            while ctr != i:
                obsolete.append(ctr)
                ctr = ctr + 1
            ctr = ctr + 1
        else:
            ctr = ctr + 1
    print "Missing syscall numbers are"
    print obsolete

def usage():
    print "USAGE: python checker.py <options>"
    print "\t -c : Sanity check and print missing syscalls"
    print "\t -syz <path to sys/netbsd>: Syzkaller checker"


def syzkaller_check(path):
    for filename in os.listdir(path):
        if filename.endswith(".txt"):
             print(os.path.join(path, filename))

def main():
    if len(sys.argv) < 2:
        usage()
        exit()
    if sys.argv[1] == '-c':
        print "Starting Sanity check"
        sanity_check()
    if sys.argv[1] == "-syz":
        if len(sys.argv) != 3:
            usage()
            exit()
        path = sys.argv[2]
        syzkaller_check(path)

if __name__ == "__main__":
    main()
