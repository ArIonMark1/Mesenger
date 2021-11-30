import dis


class Meta(type):
    """ пример метакласса, который требует, чтобы все методы снабжались строками документирования """

    def __init__(self, clsname, parents, clsdict):
        """  метод __init__(), проверяет содержимое словаря класса.
        Он отыскивает методы и проверяет, имеют ли они строки документирования """
        socket_store = []
        for key, val in clsdict.items():
            if not key.startswith('__'):
                # assert not isinstance(val, self.socket), 'Не проходит создание сокета на уровне класса'
                instructions = dis.get_instructions(val)

                for instruction in instructions:

                    if instruction.opname == 'LOAD_GLOBAL':
                        # print(instruction)
                        assert (instruction.arg == 1, instruction.argval == 'AF_INET') or (
                            instruction.arg == 2,
                            instruction.argval == 'SOCK_STREAM'), 'Доступно соединение только по TCP'

        for k, v in clsdict.items():
            if k == 'set_up':

                if socket_store:
                    forbidden_methods = ['listen', 'accept'] if clsname == 'Client' else ['connect']
                    instruct = dis.get_instructions(v)

                    for inst in instruct:
                        print('=>', inst)
                        if inst in socket_store:
                            next_inst = next(instruct)
                            assert not (
                                    next_inst.argval in forbidden_methods and next_inst.opname == 'LOAD_METHOD'), f'{clsname} не должен иметь метод {next_inst.argval}'

        type.__init__(self, clsname, parents, clsdict)
