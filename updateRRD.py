import time
import rrdtool
from getSNMP import consultaSNMP
from graphRendimiento import generarGraficaRendimiento

def actualizarRRD(comunidad, ip, documento, datos):
    ##Variables de control de umbrales
    umbralesCPU =[True, True, False]
    umbralesRAM =[False, False, False]
    umbralesOctetosEntrada = [False, False, False]

    while 1:
        paquetesUnicast = int(
            consultaSNMP(comunidad,ip,
                        '1.3.6.1.2.1.2.2.1.11.2'))
        paquetesIPV4 = int(
            consultaSNMP(comunidad,ip,
                        '1.3.6.1.2.1.4.3.0'))
        mensajesECHO = int(
            consultaSNMP(comunidad,ip,
                        '1.3.6.1.2.1.5.21.0'))
        segmentosRec = int(
            consultaSNMP(comunidad,ip,
                        '1.3.6.1.2.1.6.10.0'))
        datagramasEnt = int(
            consultaSNMP(comunidad,ip,
                        '1.3.6.1.2.1.7.1.0'))
        usoCPU = int(
            consultaSNMP(comunidad,ip, 
                        '1.3.6.1.2.1.25.3.3.1.2.196608'))
        memoriaTotal = int(
            consultaSNMP(comunidad, ip, 
                        '1.3.6.1.4.1.2021.4.5.0'))
        memoriaDisponible = int(
            consultaSNMP(comunidad, ip,
                        '1.3.6.1.4.1.2021.4.11.0')
        )
        inoctets = int(
            consultaSNMP(comunidad, ip,
                        '1.3.6.1.2.1.2.2.1.10.2')
        )        
        outoctets = int(
            consultaSNMP(comunidad, ip,
                        '1.3.6.1.2.1.2.2.1.16.2')
        )
        try:
            memoriaUtilizada = abs(memoriaTotal - memoriaDisponible)
            valor = "N:" + str(paquetesUnicast) + ':' + str(paquetesIPV4) + ':' + str(mensajesECHO) + ':' + str(segmentosRec) + ':' + str(datagramasEnt) + ':' + str(usoCPU) + ':' + str(memoriaUtilizada) + ':' + str(inoctets) + ':' + str(outoctets)
            rrdtool.update(documento, valor)
            print(valor);
            rrdtool.dump(documento,documento+'.xml')
            umbralesCPU = generarGraficaRendimiento(documento, ip, "Carga CPU", "CPU", "0", "100", 30, 50, 80, "30%", "50%", "80%", "usoCPU", umbralesCPU, datos);
            umbralesRAM = generarGraficaRendimiento(documento, ip, "Memoria RAM utilizada", "RAM", "0", "4000000", 1500000, 2000000, 3000000, "1500000Kb", "2000000Kb", "3000000Kb", "memoriaUtilizada", umbralesRAM, datos);
            #umbralesOctetosEntrada = generarGraficaRendimiento(documento, ip, "Tráfico de red de entrada", "Entrada de red", "0", "100000", 15000, 20000, 30000, "10 M", "20 M", "30 M", "inoctets", umbralesRAM, datos);
            #umbralesOctetosSalida = generarGraficaRendimiento(documento, ip, "Tráfico de red de salida", "Salida de red", "0", "100000", 15000, 20000, 30000, "10 M", "20 M", "30 M", "outoctets", umbralesRAM, datos);
            time.sleep(1)
        except Exception as e:
            print(e) 

    if ret:
        print (rrdtool.error())
        time.sleep(300)