from co import bootstrap, send
from la import setUpTransformEngine


object_vt, vtvt = bootstrap()
symbol_vt, ast_vt = setUpTransformEngine(object_vt, vtvt)

LIT = send(symbol_vt, 'allocate')
send(LIT, 'setName', 'literal')

WORD = send(symbol_vt, 'allocate')
send(WORD, 'setName', 'word')

SEQ = send(symbol_vt, 'allocate')
send(SEQ, 'setName', 'sequence')


CONTEXT = send(object_vt, 'delegated')

def emit_lit(ast, context):
  print repr(ast.data)
send(CONTEXT, 'addMethod', 'literal', emit_lit)

def emit_word(ast, context):
  print '<%s>' % (ast.data,)
send(CONTEXT, 'addMethod', 'word', emit_word)

def eval_seq(ast, context):
    for item in ast.data:
        send(item, 'eval', context)
send(CONTEXT, 'addMethod', 'sequence', eval_seq)


if __name__ == '__main__':
    from metaii import comp
    from pprint import pprint


    machine = open('metaii.asm').read()
    cola_metaii = open('cola.metaii').read()

    cola_machine = comp(cola_metaii, machine)
    source = '''
    2 4 add #
    baz 'bar' foo q #
    second first ! #
    !!k # .
    '''

##    [('k',
##  ('add', 'four', 'two'),
##  (('seq', 'foo', 'bar', 'baz'), 'first', 'second'))]

##    'b' 23 Hi ! #
##    add
##    Say goodnight Gracie #
##    Goodnight Gracie ! .
##    '''
##    
##    Goodnight Gracie !
##    ! ! c
##    .
##    '''

    body = 'def a():\n' + comp(source, cola_machine)
    print body
    exec body
    ast = a()
    pprint(ast)
    print
    send(ast[0], 'eval', CONTEXT)
