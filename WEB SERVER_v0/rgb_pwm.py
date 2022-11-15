from machine import Pin, PWM

pwmUnit = 65535/100
min = 0
max = 0

class rgb(object):
    def __init__(self, r: int, g: int, b: int, onValue: bool):
        self._pinR = PWM(Pin(r))
        self._pinG = PWM(Pin(g))
        self._pinB = PWM(Pin(b))
        self._pinR.freq(500)
        self._pinG.freq(500)
        self._pinB.freq(500)
        self._onValue = onValue

        if self._onValue == True:
            global min 
            min = -100
            global max 
            max = 65535
        elif self._onValue == False:
            global min 
            min = 65535
            global max 
            max = 0

        self._pinR.duty_u16(min)
        self._pinG.duty_u16(min)
        self._pinB.duty_u16(min)

    def off(self):
        self._pinR.duty_u16(min)
        self._pinG.duty_u16(min)
        self._pinB.duty_u16(min)

    def red(self, duty: int):
        if duty:
            self._pinR.duty_u16(normalizarValor(duty))
        else:
            self._pinR.duty_u16(max)

        self._pinG.duty_u16(min)
        self._pinB.duty_u16(min)

    def green(self, duty: int):
        self._pinR.duty_u16(min)
        if duty:
            self._pinG.duty_u16(normalizarValor(duty))
        else:
            self._pinG.duty_u16(max)
        self._pinB.duty_u16(min)

    def blue(self, duty: int):
        self._pinR.duty_u16(min)
        self._pinG.duty_u16(min)
        if duty:
            self._pinB.duty_u16(normalizarValor(duty))
        else:
            self._pinB.duty_u16(max)

    def white(self, duty: int):
        if duty:
            self._pinR.duty_u16(normalizarValor(duty))
            self._pinG.duty_u16(normalizarValor(duty))
            self._pinB.duty_u16(normalizarValor(duty))
        else:
            self._pinR.duty_u16(max)
            self._pinG.duty_u16(max)
            self._pinB.duty_u16(max)

def normalizarValor(valor: int):
        if max == 65535:
            valor = valor
        elif max == 0:
            if valor == 0:
                valor = 65535
            elif valor == 65535:
                valor = 0
            elif valor > 0 and valor < 65535:
                valor = 65535 - valor
        return valor