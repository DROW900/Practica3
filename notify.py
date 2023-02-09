from email.mime.text import MIMEText
import smtplib
from email.mime.image import MIMEImage
from email.mime.multipart import MIMEMultipart

COMMASPACE = ', '
# Define params
rrdpath = './RRD/'
imgpath = './IMG/'
fname = 'trend.rrd'

mailreceip = ""
mailserver = 'smtp.gmail.com: 587'
password = ''

def send_alert_attached(subject,rutaImagen, datos):
    """ Envía un correo electrónico adjuntando la imagen en IMG
    """
    try:
        mailsender = "";
        msg = MIMEMultipart()
        msg['Subject'] = subject
        msg['From'] = mailsender
        msg['To'] = mailreceip
        fp = open(rutaImagen, 'rb')
        img = MIMEImage(fp.read())
        fp.close()
        msg.attach(img)
        mensaje = " \n"+"IP: "+ datos['direccionIP']+"\n"+"SO: "+datos['SO']+"\n"+"Comunidad: " + datos['nombreComunidad']+ "Correo contacto: " + datos['correo']
        txt = MIMEText(mensaje, 'plain')
        msg.attach(txt);
        s = smtplib.SMTP(mailserver)
        s.starttls()
        # Login Credentials for sending the mail
        s.login(mailsender, password)

        s.sendmail(mailsender, mailreceip, msg.as_string())
        print("Se ha enviado la info")
        s.quit()
    except Exception  as e:
        print(e)
