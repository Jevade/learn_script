class VarInt(object):
    @classmethod
    def _zigzag_encode(cls, num):
        retval =  num * 2 if num >= 0 else -2 * num - 1
        return int(retval)

    @classmethod
    def _zigzag_decode(cls, num):
        retval = - (num + 1) / 2 if num % 2 else num / 2
        return int(retval)

    @classmethod
    def int_to_var(cls, num):
        num = cls._zigzag_encode(num)
        front = rear = count = 0
        while True:
            if num >> 7:
                temp = num & 0x7f
                if rear:
                    rear += (temp | 0x80) << 8
                else:
                    rear = temp
                count += 1
                num >>= 7
            else:
                front = num
                break
        if count:
            val = (front | 0x80)
            front = (front | 0x80) << count * 8
        return front + rear

print(VarInt().int_to_var(1090422))
