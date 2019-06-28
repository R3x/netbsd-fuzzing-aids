#include <test.h>

typedef struct {
        __gregset_t     __gregs;
        __greg_t        _mc_tlsbase;
        __fpregset_t    __fpregs;
} mcontext_t;

#define _UC_UCONTEXT_ALIGN      (~0xf)

/* AMD64 ABI 128-bytes "red zone". */
#define _UC_MACHINE_SP(uc)      ((uc)->uc_mcontext.__gregs[_REG_RSP] - 128)
#define _UC_MACHINE_FP(uc)      ((uc)->uc_mcontext.__gregs[_REG_RBP])
#define _UC_MACHINE_PC(uc)      ((uc)->uc_mcontext.__gregs[_REG_RIP])
#define _UC_MACHINE_INTRV(uc)   ((uc)->uc_mcontext.__gregs[_REG_RAX])

typedef struct {
        __fpregset_t    __fpregs;
} test_struct;

#define _UC_MACHINE_SET_PC(uc, pc)      _UC_MACHINE_PC(uc) = (pc)

#define _UC_TLSBASE     0x00080000
