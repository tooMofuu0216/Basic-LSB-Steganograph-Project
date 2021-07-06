import cv2
import wave


class Stegano:
    def __init__(self):
        self.delimiter = '$_this15End_$'

    def hide(self, file_name, payload):
        pass

    def extract(self, file_name):
        pass


# transform to png
class SteganoImg(Stegano):
    def __init__(self):
        super().__init__()

    # hide msg and save as PNG
    def hide(self, file_name, payload):
        img = cv2.imread(file_name)
        # delimit str
        payload += self.delimiter
        new_img = self.modify_pixel(img, payload)
        file_path = file_name.split('.')[0]
        cv2.imwrite(file_path + '_out.PNG', new_img)

    # change lsb of pixel bytes from binary string of payload
    def modify_pixel(self, img, payload):
        binary_msg = list(map(int, ''.join([format(ord(char), '08b') for char in payload])))
        bin_msg_len = len(binary_msg)
        if bin_msg_len > img.shape[0] * img.shape[1] * img.shape[-1]:
            raise ValueError('Message too long for image!!')
        # index to extrack bits from binary string
        bit_str_count = 0
        # row, col = height,width; col => tuple of bgr pixel
        for row in img:
            for col in row:
                for idx, pix_val in enumerate(col):
                    if bit_str_count >= bin_msg_len:
                        return img
                    # clear lsb of pix_val by bitwise &, set lsb from binary_msg
                    col[idx] = pix_val & 254 | binary_msg[bit_str_count]
                    bit_str_count += 1

    def extract(self, file_name):
        img = cv2.imread(file_name)
        binary_msg = []
        for row in img:
            for col in row:
                # strip lsb by bitwise &
                b, g, r = (pix_val & 1 for pix_val in col)
                binary_msg.append(b)
                binary_msg.append(g)
                binary_msg.append(r)

        # byte -> int -> char (ASCII)
        string = "".join(chr(int("".join(map(str, binary_msg[i:i + 8])), 2)) for i in range(0, len(binary_msg), 8))
        decoded = string.split(self.delimiter)[0]
        print("Img Msg: " + decoded)


# wav 2 wav
class SteganoSound(Stegano):
    def __init__(self):
        super().__init__()

    def hide(self, file_name, payload):
        song = wave.open(file_name, mode='rb')
        # get wav to bytearray
        sound_bytes = bytearray((song.readframes(-1)))
        payload += self.delimiter
        # change all message bytes to int
        bits = list(map(int, ''.join([format(ord(i), '08b') for i in payload])))
        msg_len = len(bits)
        if len(sound_bytes) < msg_len:
            raise ValueError('Message too long!!')

        # clear and set lsb of each music bytes using bitwise &, |
        for i, bit in enumerate(bits):
            sound_bytes[i] = (sound_bytes[i] & 254) | bit
        frame_modified = bytes(sound_bytes)

        file_path = file_name.split('.')[0]
        with wave.open(file_path + '_out.wav', 'wb') as fd:
            fd.setparams(song.getparams())
            fd.writeframes(frame_modified)
        song.close()

    def extract(self, file_name):
        song = wave.open(file_name, mode='rb')
        sound_bytes = bytearray((song.readframes(-1)))
        # get lsb from wav
        extracted = [sound_bytes[i] & 1 for i in range(len(sound_bytes))]
        # byte -> int -> char (ASCII)
        string = "".join(chr(int("".join(map(str, extracted[i:i + 8])), 2)) for i in range(0, len(extracted), 8))
        decoded = string.split(self.delimiter)[0]
        print("Sound Msg: " + decoded)
        song.close()


if __name__ == '__main__':
    i_stegano = SteganoImg()
    i_stegano.hide('resource/input.JPG', 'heLLo World!')
    i_stegano.extract('resource/input'+'_out.PNG')
    s_stegano = SteganoSound()
    s_stegano.hide('resource/Pack#2_Kit 1_Groove 1_180BPM.wav', 'heLLo World!')
    s_stegano.extract('resource/Pack#2_Kit 1_Groove 1_180BPM'+'_out.wav')
