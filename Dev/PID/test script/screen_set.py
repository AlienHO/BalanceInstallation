from pyb import Pin, SPI
from sensor import set_vflip,set_hmirror

spi=SPI(2,SPI.MASTER,baudrate=70000000)
cs=Pin('PD10', Pin.OUT_PP)
rst=Pin('PD8', Pin.OUT_PP)
rs =Pin('PD9', Pin.OUT_PP)
set_vflip(True)     #翻转画面
set_hmirror(True)
def write_c(c):
    cs.low()
    rs.low()
    spi.send(c)
    cs.high()

def write_d(c):
    cs.low()
    rs.high()
    spi.send(c)
    cs.high()

write_c(0x36)#设置屏幕方向
write_d(0x60)
