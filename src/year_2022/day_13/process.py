import itertools
import operator
import lark


DIVIDER_PACKET_1 = "[[2]]"
DIVIDER_PACKET_2 = "[[6]]"


class Packet(list):
    def __lt__(self, other):
        return self._cmp(other, operator.lt)

    def __le__(self, other):
        return NotImplemented

    def __gt__(self, other):
        return self._cmp(other, operator.gt)

    def __ge__(self, other):
        return NotImplemented

    def __eq__(self, other):
        return NotImplemented

    def __ne__(self, other):
        return NotImplemented

    def _cmp(self, other, cmp_fn):
        if cmp_fn is operator.lt:
            opp_cmp_fn = operator.gt
        elif cmp_fn is operator.gt:
            opp_cmp_fn = operator.lt
        else:
            raise ValueError

        if isinstance(other, int):
            other = Packet([other])

        for pair in itertools.zip_longest(self, other):
            match pair:
                case [int() as left, int() as right] | [
                    Packet() as left,
                    Packet() as right,
                ]:
                    if result := cmp_fn(left, right):
                        return result
                    elif result := opp_cmp_fn(left, right):
                        return not result

                case [None, (Packet() | int())]:
                    # left higher-level list was shorter than right higher-level list
                    return cmp_fn is operator.lt

                case [(Packet() | int()), None]:
                    # left higher-level list was longer than right higher-level list
                    return cmp_fn is operator.gt

                case [Packet() as left, int() as right]:
                    if result := cmp_fn(left, Packet([right])):
                        return result
                    elif result := opp_cmp_fn(left, Packet([right])):
                        return not result

                case [int() as left, Packet() as right]:
                    if result := cmp_fn(Packet([left]), right):
                        return result
                    elif result := opp_cmp_fn(Packet([left]), right):
                        return not result

                case _:
                    raise Exception
        return False


PKT_GRAMMAR = r"""\
    ?start : list
    
    list   : "[" [value ("," value)*] "]"
    ?value : list 
           | INT  -> integer

    %import common.INT
    %import common.WS
    %ignore WS
"""


class PacketTransformer(lark.Transformer):
    list = Packet
    integer = lark.v_args(inline=True)(int)


pkt_parser = lark.Lark(
    PKT_GRAMMAR,
    parser="lalr",
    maybe_placeholders=False,
    transformer=PacketTransformer(),
)

parse = pkt_parser.parse


class DistressSignal:
    def __init__(self, sig_in):
        self.pkt_pairs = [
            Packet([parse(raw_packet) for raw_packet in packet_pair.splitlines()])
            for packet_pair in sig_in.strip().split("\n\n")
        ]

        sig = [pkt for pkt_pair in self.pkt_pairs for pkt in pkt_pair]
        self.div_pkt_1 = parse(DIVIDER_PACKET_1)
        self.div_pkt_2 = parse(DIVIDER_PACKET_2)
        sig.extend([self.div_pkt_1, self.div_pkt_2])
        self.sig = sorted(sig)

    @classmethod
    def read_file(cls) -> "DistressSignal":
        with open("input.txt") as f:
            return cls(f.read().strip())

    def valid_pkt_pair_idxs(self):
        return [
            idx
            for idx, pkt_pair in enumerate(self.pkt_pairs, start=1)
            if pkt_pair[0] < pkt_pair[1]
        ]

    def sum_valid_pair_idx(self):
        return sum(self.valid_pkt_pair_idxs())

    def find_decoder_key(self):
        idx_1 = self.sig.index(self.div_pkt_1) + 1
        idx_2 = self.sig.index(self.div_pkt_2) + 1
        return idx_1 * idx_2


def main() -> None:
    signal = DistressSignal.read_file()

    print(
        "Sum of indices of packet pairs in correct order:", signal.sum_valid_pair_idx()
    )
    print("Decoder key for distress signal:", signal.find_decoder_key())


if __name__ == "__main__":
    import timeit

    print(timeit.timeit(main, number=1))
