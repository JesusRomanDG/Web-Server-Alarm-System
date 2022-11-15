from machine import Pin, Timer
import utime
import rgb_pwm
import socket

tiempoCalibracionPir = 3000
count = 0
countActWebServer = 0
delayAlarm = 500
bool_status_alarma = False
bool_alarma = False
bool_buzzer = False
bool_led = False
tmr_alarma = Timer()

btn = Pin(11, Pin.IN, Pin.PULL_UP)

rgbObj = rgb_pwm.rgb(13, 14, 15, False)
rgbObj.off()

buzzer = Pin(12, Pin.OUT)
buzzer.off()

pir = Pin(21, Pin.IN, Pin.PULL_DOWN)

def calibrarPir():
    utime.sleep_ms(tiempoCalibracionPir)
    print("Calibracion terminada")
    rgbObj.green(1000)

calibrarPir()

def interrupcion_pir(pin):
    global bool_status_alarma
    global count
    
    if pin.value():
        count += 1
        print("Alarma! Movimiento detectado!" + str(count))
        tmr_alarma.init(period=delayAlarm, mode=Timer.PERIODIC, callback=lambda t: encender_alarma())
        bool_status_alarma = True
        
pir.irq(handler=interrupcion_pir, trigger=Pin.IRQ_RISING)

def apagar_alarma(origin: str):
    global bool_status_alarma
    global countActWebServer
    
    if (origin=="webserver" and countActWebServer==0):
        bool_status_alarma = False
        rgbObj.red(-100)
        buzzer.off()
        rgbObj.green(1000)
        count+=1
    elif (origin!="btn"):
        bool_status_alarma = False
        rgbObj.red(-100)
        buzzer.off()
        rgbObj.green(1000)

btn.irq(handler=apagar_alarma, trigger=Pin.IRQ_FALLING)
        
def encender_alarma():
    global bool_status_alarma
    global bool_alarma
    
    if bool_status_alarma == True:
        if bool_alarma==False:
            rgbObj.red(1000)
            buzzer.on()
        else:
            rgbObj.red(-100)
            buzzer.off()
        bool_alarma = not bool_alarma

def get_string_value(input: str):
    global bool_status_alarma
    global count
    cadena = ""
    
    if input=="alarma":
        if bool_status_alarma==True:
            cadena = "<p>!ADVERTENCIA! !La alarma ha sido activada!<br>Puedes presionar el boton para desactivar la alarma.</p>"
        else:
            cadena = "La alarma no esta activada."
    elif input=="led":
        if bool_status_alarma==True:
            cadena = "LED parpadeando en rojo"
        else:
            cadena = "LED encendido en verde"
    elif input == "buzzer":
        if bool_status_alarma==True:
            cadena = "Buzzer sonando"
        else:
            cadena = "Buzzer desactivado"
    elif input == "pir":
        cadena = "Veces que el sensor ha detectado movimiento: " + str(count)
    return str(cadena)     

def web_page():
    
    html = """
            <!doctype html>
            <html lang="es">
            <head>
            <title>Raspberry Pi Pico W Web Server</title>
            <meta charset="utf-8">
            <meta name="viewport" content="width=device-width, initial-scale=1">
            <link rel="icon" href="data:,">
            <link href="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/css/bootstrap.min.css" rel="stylesheet" integrity="sha384-Zenh87qX5JnK2Jl0vWa8Ck2rdkQ2Bzep5IDxbcnCeuOxjzrPF/et3URy9Bv1WTRi" crossorigin="anonymous">
            <style>
                html {
                    font-family: Helvetica;
                    display: inline-block;
                    margin: 0px auto;
                    text-align: center;
                }
                h1 {
                    color: #0F3376;
                    padding: 2vh;
                }
                p {
                    font-size: 1.5rem;
                }
                table {
                    margin: auto;            
                }
                td{
                    padding: 10px ;
                } 
                .Button {           
                    border-radius: 31px;           
                    display: inline-block;
                    cursor: pointer;
                    color: #ffffff;
                    font-family: Arial;
                    font-size: 17px;
                    font-weight: bold;
                    font-style: italic;
                    font-color: #000000;
                    padding: 17px 19px;
                    text-decoration: none;
                    background-color: #848484;            
                    border: 6px solid #000000;           
                    text-shadow: 0px 2px 2px #471e1e;
                }
                
                .Button:hover {
                    background-color: #f51616;
                }
                
                .ButtonR {
                    background-color: #ec4949;            
                    border: 6px solid #991f1f;           
                    text-shadow: 0px 2px 2px #471e1e;
                }
                .ButtonR:hover {
                    background-color: #f51616;
                }

                .Button:active {
                    position: relative;
                    top: 1px;
                }
                .ButtonG {
                    background-color: #49ec56;            
                    border: 6px solid #23991f;          
                    text-shadow: 0px 2px 2px #1e4723;
                }
                .ButtonG:hover {
                    background-color: #29f516;
                }  
                .ButtonB {
                    background-color: #4974ec;           
                    border: 6px solid #1f3599;         
                    text-shadow: 0px 2px 2px #1e2447;
                }
                .ButtonB:hover {
                    background-color: #165df5;
                }
            
            </style>
                <script>
                    setInterval(updateValues, 10000);
            
                    function updateValues() {
                        location.reload(); 
                    }
                </script>
            </head>

            <body>
                <h1><span class="badge text-bg-dark">Raspberry Pi Pico W Web Server</span></h1>
                <h1><span class="badge text-bg-dark">Control de sistema de alarma</span></h1>
                <center>
                    <p style="text-align:center">
                        <span class="badge text-bg-dark">
                            Elaborado por: Dominguez Garcia Jesus Roman
                            <br>Usuario de GitHub: JesusRomanDG
                            <br>Fecha: 15 de noviembre de 2022
                            <br>Descripcion: Los valores del sistema de alarma se
                            <br>muestran en la interfaz web server, en la que se puede
                            <br>visualizar si el led y/o el buzzer estan activados.
                            <br>Asi mismo muestra el numero de veces que el sensor PIR
                            <br>ha detectado movimiento.
                        </span>
                    </p>
                </center>
                <table>
                    <tbody>
                        <tr>
                            <td colspan="2">
                                <center>
                                    <strong>Link repositorio:<a href="https://github.com/JesusRomanDG/Web-Server-Alarm-System">https://github.com/JesusRomanDG/Web-Server-Alarm-System</a></strong>  
                                </center>
                            </td>
                        </tr>
                        <tr>
                            <td colspan="2">
                                <center>
                                    <p><a href="/disable"><button class="Button">ALARMA</button></a></p>
                                </center>
                            </td>
                        </tr>
                        <tr>
                            <td colspan="2">
                                <center>
                                    <strong> """+ get_string_value("alarma") +""" </strong>  
                                </center>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <center>
                                    <p><a href="/update"><button class="ButtonR Button">LED</button></a></p>
                                </center>
                            </td>
                            <td>
                                <center>
                                    <strong> """+ get_string_value("led") +""" </strong>
                                </center>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <center>
                                    <p><a href="/update"><button class="ButtonG Button">BUZZER</button></a></p>
                                </center>   
                            </td>
                            <td>
                                <center>
                                    <strong> """+ get_string_value("buzzer") +""" </strong>
                                </center>
                            </td>
                        </tr>
                        <tr>
                            <td>
                                <center>
                                    <p><a href="/update"><button class="ButtonB Button">PIR</button></a></p>
                                </center>
                            </td>
                            <td>
                                <center>
                                    <strong> """+ get_string_value("pir") +""" </strong>
                                </center>   
                            </td>
                        </tr>
                        <tr>
                            <td colspan="2">
                                <center>
                                    <img src="http://drive.google.com/uc?export=view&id=1_Wju3ZMWgcBYE2P7FpOpm3hxFN6DmeWg" alt="Circuito" width="500" height="400">
                                </center>
                            </td>
                        </tr>
                        <tr>
                            <td colspan="2">
                                <center>
                                    <img src="http://drive.google.com/uc?export=view&id=1b0pAs2Gl0bY1pBU1dywA14xvyeS0ence" alt="Logo Raspberry Pi" width="90" height="120">
                                    <img src="http://drive.google.com/uc?export=view&id=1IO3CfxwxK56UYkiFSwGAXzryjjkn89cM" alt="Logo One Line Code" width="150" height="120">
                                </center>
                            </td>
                        </tr>
                        <tr>
                            <td colspan="2">
                                <center>
                                    <p>Propiedad de OLC, 2022. Todos los derechos reservados.</p>
                                </center>
                            </td>
                        </tr>
                    </tbody>
                </table>
                <script src="https://cdn.jsdelivr.net/npm/bootstrap@5.2.2/dist/js/bootstrap.bundle.min.js" integrity="sha384-OERcA2EqjJCMA+/3y+gxIOqMEjwtxJY7qPCqsdltbNJuaOe923+mo//f6V8Qbsw3" crossorigin="anonymous"></script>
            </body>
            </html>
        """
    return html


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s.bind(('', 80))
s.listen(5)

while True:
    
    try:
        conn, addr = s.accept()
        print('Got a connection from %s' % str(addr))
        request = conn.recv(1024)
        request = str(request)   
        update = request.find('/update')
        disable = request.find('/disable')
        
        if update == 6:
            print('update')
        
        if disable > -1:
            print('disable')
            
            apagar_alarma("webserver")
        
        response = web_page()
        conn.send('HTTP/1.1 200 OK\n')
        conn.send('Content-Type: text/html\n')
        conn.send('Connection: close\n\n')
        conn.sendall(response)
        conn.close()
    except Exception as e:
        print(e)