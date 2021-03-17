from pkg_resources import resource_filename
import click

from sidh.common import attrdict, geometric_serie, rounds
from sidh.constants import strategy_data

@click.command()
@click.pass_context
def bsidh_main(ctx):
    algo = ctx.meta['sidh.kwargs']['algo']
    setting = ctx.meta['sidh.kwargs']
    coeff = algo.curve.coeff
    SQR, ADD = algo.curve.SQR, algo.curve.ADD
    init_runtime = algo.basefield.init_runtime
    validate = algo.curve.issupersingular
    measure = algo.curve.measure
    strategy_at_6_A = algo.strategy.strategy_at_6_A
    strategy_at_6_B = algo.strategy.strategy_at_6_B
    strategy_A = algo.strategy.strategy_A
    strategy_B = algo.strategy.strategy_B
    random_scalar_A = algo.strategy.random_scalar_A
    random_scalar_B = algo.strategy.random_scalar_B

    print(
        "// The running time is assuming S = %1.2f x M and a = %1.2f x M, and giving in millions of field operations.\n"
        % (SQR, ADD)
    )

    ''' -------------------------------------------------------------------------------------
        Main
        ------------------------------------------------------------------------------------- '''

    # ------------------------------------------------------------------------- Alice
    print("// --- \033[0;35mAlice\033[0m")
    init_runtime()
    a_private = random_scalar_A()
    a_public = strategy_at_6_A(a_private)

    print(
        "// Running time (Strategy evaluation):\t\t\t%2.3fM + %2.3fS + %2.3fa = %2.3fM;"
        % (
            algo.basefield.fpmul / (10.0 ** 6),
            algo.basefield.fpsqr / (10.0 ** 6),
            algo.basefield.fpadd / (10.0 ** 6),
            measure([algo.basefield.fpmul, algo.basefield.fpsqr, algo.basefield.fpadd]) / (10.0 ** 6),
        )
    )
    print("sk_a := %d;" % a_private)
    print("pk_a := %s;" % coeff(a_public))

    # ------------------------------------------------------------------------- Bob
    print("\n// --- \033[0;34mBob\033[0m")
    init_runtime()
    b_private = random_scalar_B()
    b_public = strategy_at_6_B(b_private)
    
    print(
        "// Running time (Strategy evaluation):\t\t\t%2.3fM + %2.3fS + %2.3fa = %2.3fM;"
        % (
            algo.basefield.fpmul / (10.0 ** 6),
            algo.basefield.fpsqr / (10.0 ** 6),
            algo.basefield.fpadd / (10.0 ** 6),
            measure([algo.basefield.fpmul, algo.basefield.fpsqr, algo.basefield.fpadd]) / (10.0 ** 6),
        )
    )
    print("sk_b := %d;" % b_private)
    print("pk_b := %s;" % coeff(b_public))

    print("\n// ===================== \033[0;33mSecret Sharing Computation\033[0m")
    # ------------------------------------------------------------------------- Alice
    print("// --- \033[0;35mAlice\033[0m")
    init_runtime()
    #public_validation = validate(b_public)
    #assert public_validation
    
    print(
        "// Running time (key validation):\t%2.3fM + %2.3fS + %2.3fa = %2.3fM,"
        % (
            algo.basefield.fpmul / (10.0 ** 6),
            algo.basefield.fpsqr / (10.0 ** 6),
            algo.basefield.fpadd / (10.0 ** 6),
            measure([algo.basefield.fpmul, algo.basefield.fpsqr, algo.basefield.fpadd]) / (10.0 ** 6),
        )
    )

    init_runtime()
    ss_a = strategy_A(a_private, b_public)
    print(
        "// Running time (Strategy evaluation + key validation):\t%2.3fM + %2.3fS + %2.3fa = %2.3fM;"
        % (
            algo.basefield.fpmul / (10.0 ** 6),
            algo.basefield.fpsqr / (10.0 ** 6),
            algo.basefield.fpadd / (10.0 ** 6),
            measure([algo.basefield.fpmul, algo.basefield.fpsqr, algo.basefield.fpadd]) / (10.0 ** 6),
        )
    )
    print("ss_a := %s;\n" % coeff(ss_a))

    # ------------------------------------------------------------------------- Bob
    print("// --- \033[0;34mBob\033[0m")
    init_runtime()
    #public_validation = validate(a_public)
    #assert public_validation
    
    print(
        "// Running time (key validation):\t%2.3fM + %2.3fS + %2.3fa = %2.3fM,"
        % (
            algo.basefield.fpmul / (10.0 ** 6),
            algo.basefield.fpsqr / (10.0 ** 6),
            algo.basefield.fpadd / (10.0 ** 6),
            measure([algo.basefield.fpmul, algo.basefield.fpsqr, algo.basefield.fpadd]) / (10.0 ** 6),
        )
    )

    init_runtime()
    ss_b = strategy_B(b_private, a_public)
    
    print(
        "// Running time (Strategy evaluation + key validation):\t%2.3fM + %2.3fS + %2.3fa = %2.3fM;"
        % (
            algo.basefield.fpmul / (10.0 ** 6),
            algo.basefield.fpsqr / (10.0 ** 6),
            algo.basefield.fpadd / (10.0 ** 6),
            measure([algo.basefield.fpmul, algo.basefield.fpsqr, algo.basefield.fpadd]) / (10.0 ** 6),
        )
    )
    print("ss_b := %s;" % coeff(ss_b))

    try:
        assert(coeff(ss_a) == coeff(ss_b))
        print('\n\x1b[0;30;43m' + 'Successfully passed!' + '\x1b[0m')
    except:
        raise TypeError(
            '\x1b[0;30;41m'
            + 'Great Scott!... The sky is falling. NOT PASSED!!!'
            + '\x1b[0m'
        )

    return attrdict(name='bsidh-main', **locals())
