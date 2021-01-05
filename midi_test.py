import mido
import random

with mido.open_output('IAC Driver Bus 1') as port:
    msg = mido.Message('note_on')
    msg.note = random.randint(21,108)
    port.send(msg)