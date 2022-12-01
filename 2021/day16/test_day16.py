import math

INPUT = '40541D900AEDC01A88002191FE2F45D1006A2FC2388D278D4653E3910020F2E2\
F3E24C007ECD7ABA6A200E6E8017F92C934CFA0E5290B569CE0F4BA5180213D963C00DC4001\
0A87905A0900021B0D624C34600906725FFCF597491C6008C01B0004223342488A200F4378C\
9198401B87311A0C0803E600FC4887F14CC01C8AF16A2010021D1260DC7530042C012957193\
779F96AD9B36100907A00980021513E3943600043225C1A8EB2C3040043CC3B1802B400D3CA\
4B8D3292E37C30600B325A541D979606E384B524C06008E802515A638A73A226009CDA5D802\
6200D473851150401E8BF16E2ACDFB7DCD4F5C02897A5288D299D89CA6AA672AD5118804F59\
2FC5BE8037000042217C64876000874728550D4C0149F29D00524ACCD2566795A0D880432BE\
AC79995C86483A6F3B9F6833397DEA03E401004F28CD894B9C48A34BC371CF7AA840155E002\
012E21260923DC4C248035299ECEB0AC4DFC0179B864865CF8802F9A005E264C25372ABAC8D\
EA706009F005C32B7FCF1BF91CADFF3C6FE4B3FB073005A6F93B633B12E0054A124BEE9C570\
004B245126F6E11E5C0199BDEDCE589275C10027E97BE7EF330F126DF3817354FFC82671BB5\
402510C803788DFA009CAFB14ECDFE57D8A766F0001A74F924AC99678864725F253FD134400\
F9B5D3004A46489A00A4BEAD8F7F1F7497C39A0020F357618C71648032BB004E4BBC4292EF1\
167274F1AA0078902262B0D4718229C8608A5226528F86008CFA6E802F275E2248C65F36100\
66274CEA9A86794E58AA5E5BDE73F34945E2008D27D2278EE30C489B3D20336D00C2F002DF4\
80AC820287D8096F700288082C001DE1400C50035005AA2013E5400B10028C009600A74001E\
F2004F8400C92B172801F0F4C0139B8E19A8017D96A510A7E698800EAC9294A6E985783A400\
AE4A2945E9170'


def hex_to_bin(s) -> str:
    num = int(s, 16)
    return f'{num:04b}'


def decode_hex(s) -> str:
    bits = ''
    for ch in s:
        bits = bits + hex_to_bin(ch)
    return bits


def bin_to_dec(s) -> int:
    return int(s, 2)


def decode_header(bits):
    version = bin_to_dec(bits[0:3])
    typeid = bin_to_dec(bits[3:6])
    remainder = bits[6:]
    return (version, typeid, remainder)


def decode_literal(s):
    num, more = '', True
    while more:
        more = s[0] == '1'
        num = num + s[1:5]
        s = s[5:]
    return (bin_to_dec(num), s)


def version_sum(s):
    root_packet = decode_packet('0x' + s)
    return get_version_sum(root_packet)


def get_version_sum(packet):
    result = packet.version
    for p in packet.sub:
        result += get_version_sum(p)
    return result


class Packet:
    def __init__(self, version, typeid, num=None, length_type_id=None) -> None:
        self.version = version
        self.typeid = typeid
        self.num = num
        self.length_type_id = length_type_id
        self.sub = []

    def tuple(self):
        if self.typeid == 4:  # literal
            return (self.version, self.typeid, self.num)
        subs = [packet.tuple() for packet in self.sub]
        return (self.version, self.typeid, self.num, self.length_type_id, subs)


def decode_packet(s):
    if s.startswith('0x'):
        s = decode_hex(s[2:])

    packet, _ = decode_packetr(s)
    return packet


def decode_packetr(s):
    # root packet
    (version, typeid, r) = decode_header(s[:6])

    s = s[6:]

    if typeid == 4:  # literal
        num, r = decode_literal(s)
        packet = Packet(version, typeid, num)
        return (packet, r)

    length_type_id = int(s[0])

    if length_type_id == 0:
        # next 15 bits are a number that represents the total length in bits of
        # the sub-packets contained by this packet.
        x = bin_to_dec(s[1:16])
        s = s[16:]
        r = s[x:]
        s = s[:x]

        packet = Packet(version, typeid, 0, length_type_id)
        while len(s) > 0:
            p, s = decode_packetr(s)
            packet.sub.append(p)
        packet.num = len(packet.sub)
        if typeid > 4:
            assert packet.num > 1
        return (packet, s + r)

    if length_type_id == 1:
        # next 11 bits are a number that represents the number of sub-packets immediately
        # contained by this packet.
        num = bin_to_dec(s[1:12])
        s = s[12:]
        # r = ???
        # expect num packets to follow in s...
        packet = Packet(version, typeid, num, length_type_id)
        for _ in range(num):
            p, s = decode_packetr(s)
            packet.sub.append(p)
        if typeid > 4:
            assert packet.num > 1
        return (packet, s)

    raise ValueError('ooops')


def resolve(packet):
    match packet.typeid:
        case 0:  # '+'
            return sum([resolve(p) for p in packet.sub])
        case 1:
            return math.prod([resolve(p) for p in packet.sub])
        case 2:
            return min([resolve(p) for p in packet.sub])
        case 3:
            return max([resolve(p) for p in packet.sub])
        case 4:
            return packet.num
        case 5:
            assert len(packet.sub) == 2
            return 1 if resolve(packet.sub[0]) > resolve(packet.sub[1]) else 0
        case 6:
            assert len(packet.sub) == 2
            return 1 if resolve(packet.sub[0]) < resolve(packet.sub[1]) else 0
        case 7:
            assert len(packet.sub) == 2
            return 1 if resolve(packet.sub[0]) == resolve(packet.sub[1]) else 0
    raise ValueError(f'unknown packet typeid: {packet.typeid}')


def calc(s):
    root_packet = decode_packet('0x' + s)
    return resolve(root_packet)


def test_sample():
    assert hex_to_bin('F') == '1111'
    assert hex_to_bin('0xF') == '1111'
    assert hex_to_bin('0') == '0000'
    assert bin_to_dec('011111100101') == 2021
    assert decode_hex('D2FE28') == '110100101111111000101000'
    assert decode_header(decode_hex('D2FE28')) == (6, 4, '101111111000101000')
    assert decode_literal('101111111000101000') == (2021, '000')


def test_version_sum():
    assert version_sum('8A004A801A8002F478') == 16
    assert version_sum('620080001611562C8802118E34') == 12
    assert version_sum('C0015000016115A2E0802F182340') == 23
    assert version_sum('A0016C880162017C3686B18A3D4780') == 31


def test_version_sum_input():
    assert version_sum(INPUT) == 945


def test_decode_packet():
    assert decode_header(decode_hex('D2FE28')) == (6, 4, '101111111000101000')
    assert decode_packet('0xD2FE28').tuple() == (6, 4, 2021)


def test_oper_type0():
    # operator with length type 0 and two-sub literal packets:
    assert decode_packet('0x38006F45291200').tuple() == (1, 6, 2, 0, [
        (6, 4, 10),
        (2, 4, 20)
    ])


def test_oper_type1():
    # operator with length type 1 and three sub-packets:
    assert decode_packet('0xEE00D40C823060').tuple() == (7, 3, 3, 1, [
        (2, 4, 1),
        (4, 4, 2),
        (1, 4, 3)
    ])


def test_nested():
    packet = decode_packet('0x9C0141080250320F1802104A08')  # 1 + 3 == 2 * 2
    version, typeid, num, length_type_id, subs = packet.tuple()

    assert (version, typeid, num, length_type_id) == (
        4, 7, 2, 0)  # type 7 is ==
    assert len(subs) == 2
    assert subs[0] == (2, 0, 2, 1, [  # + is typeid 0
        (2, 4, 1),  # literal 1
        (4, 4, 3),  # literal 3
    ])
    assert subs[1] == (6, 1, 2, 1, [  # * is typeid 1
        (0, 4, 2),  # literal 2
        (2, 4, 2),  # literal 2
    ])


def test_calc():
    assert calc('C200B40A82') == 3
    assert calc('04005AC33890') == 54
    assert calc('880086C3E88112') == 7
    assert calc('CE00C43D881120') == 9
    assert calc('D8005AC2A8F0') == 1
    assert calc('F600BC2D8F') == 0
    assert calc('9C005AC2F8F0') == 0
    assert calc('9C0141080250320F1802104A08') == 1


def test_calc_input():
    assert calc(INPUT) == 10637009915279
