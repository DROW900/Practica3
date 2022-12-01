#!/usr/bin/env python
import rrdtool
def generarRRD(nombre):
    ret = rrdtool.create(str(nombre),
                        "--start",'N',
                        "--step",'300',
                        "DS:paquetesUnicast:COUNTER:120:U:U",
                        "DS:paquetesIPV4:COUNTER:120:U:U",
                        "DS:mensajesECHO:COUNTER:120:U:U",
                        "DS:segmentosRecibidos:COUNTER:120:U:U",
                        "DS:datagramasUDP:COUNTER:120:U:U",
                        "DS:usoCPU:GAUGE:60:0:100",
                        "DS:memoriaUtilizada:GAUGE:60:U:U",
                        "DS:inoctets:COUNTER:120:U:U",
                        "DS:outoctets:COUNTER:120:U:U",
                        "RRA:AVERAGE:0.5:1:100",
                        "RRA:AVERAGE:0.5:1:100",
                        "RRA:AVERAGE:0.5:1:100",
                        "RRA:AVERAGE:0.5:1:100",
                        "RRA:AVERAGE:0.5:1:100",
                        "RRA:AVERAGE:0.5:1:2100",
                        "RRA:MAX:0.5:1:2100",
                        "RRA:AVERAGE:0.5:1:2100",
                        "RRA:AVERAGE:0.5:1:2100")

    if ret:
        print (rrdtool.error())