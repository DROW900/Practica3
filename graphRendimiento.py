import rrdtool
import time
from notify import send_alert_attached
#30   1,500,000
#50   2,000,000
#90   3,000,000

def generarGraficaRendimiento(documento, 
                              ip, 
                              tituloVertical,
                              dispositivo, 
                              limiteInferior, 
                              limiteSuperior,
                              primerUmbral,
                              segundoUmbral,
                              tercerUmbral,
                              unidadValorPrimerUmbral,
                              unidadValorSegundoUmbral,
                              unidadValorTercerUmbral,
                              variableRRD,
                              validacionesNotificaciones,
                              datos): 
    try:
        ultima_lectura = int(rrdtool.last(documento))
        tiempo_final = ultima_lectura
        tiempo_inicial = tiempo_final - 1800
        ret = rrdtool.graphv( ip+dispositivo+".png", ##Permite extraer la info y regresar el valor
                            "--start",str(tiempo_inicial),
                            "--end",str(tiempo_final),
                            "--vertical-label="+tituloVertical,
                            '--lower-limit', str(limiteInferior),
                            '--upper-limit', str(limiteSuperior),
                            "--title=Carga de "+ dispositivo + " del agente "+ ip +". Usando SNMP y RRDtools \n Detección de umbrales",
                            "DEF:cargaDispositivo="+documento+":"+variableRRD+":AVERAGE",
                            "VDEF:cargaLAST=cargaDispositivo,LAST",
                            "CDEF:umbralPrimero=cargaDispositivo," + str(primerUmbral) + ",LT,0,cargaDispositivo,IF",
                            "CDEF:umbralSegundo=cargaDispositivo," + str(segundoUmbral) + ",LT,0,cargaDispositivo,IF",
                            "CDEF:umbralTercero=cargaDispositivo," + str(tercerUmbral) + ",LT,0,cargaDispositivo,IF",
                            "AREA:cargaDispositivo#00FF00:Carga del "+ dispositivo,
                            "AREA:umbralPrimero#FF9F00:Carga " + dispositivo + " mayor que " + str(primerUmbral),
                            "AREA:umbralSegundo#FF6F00:Carga " + dispositivo + " mayor que " + str(segundoUmbral),
                            "AREA:umbralTercero#FF3F00:Carga " + dispositivo + " mayor que " + str(tercerUmbral),
                            "HRULE:"+str(primerUmbral)+"#FF0000:Umbral "+unidadValorPrimerUmbral,
                            "HRULE:"+str(segundoUmbral)+"#FF0000:Umbral "+unidadValorSegundoUmbral,
                            "HRULE:"+str(tercerUmbral)+"#FF0000:Umbral "+unidadValorTercerUmbral,
                            "PRINT:cargaLAST:%6.2lf")

        ultimo_valor=float(ret['print[0]'])
        if ultimo_valor>primerUmbral:
            if validacionesNotificaciones[0] != True:
                send_alert_attached("Sobrepasa el primer umbral" + unidadValorPrimerUmbral + " de " + dispositivo, ip+dispositivo+".png", datos)
                validacionesNotificaciones[0] = True;
        if ultimo_valor>segundoUmbral:
            if validacionesNotificaciones[1] != True:
                send_alert_attached("Sobrepasa el segundo umbral" + unidadValorSegundoUmbral + " de " + dispositivo, ip+dispositivo+".png", datos)
                validacionesNotificaciones[1] = True;
        if ultimo_valor>tercerUmbral:
            if validacionesNotificaciones[2] != True:
                send_alert_attached("Sobrepasa el tercer umbral: " + unidadValorTercerUmbral + " de " + dispositivo, ip+dispositivo+".png", datos)
                validacionesNotificaciones[2] = True;
        return validacionesNotificaciones;
    except Exception as e:
        print(e)
