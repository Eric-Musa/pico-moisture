import _thread
from machine import UART, ADC, Pin
import time


soil = ADC(Pin(26))
 
#Calibraton values

def read_moisture(max_moisture_adc=19200, min_moisture_adc=49300):
    adc_val = soil.read_u16()
    moisture = (min_moisture_adc-adc_val)*100/(min_moisture_adc-max_moisture_adc) 
    return {"moisture": moisture, "adc": adc_val, "timestamp": time.time()}
    # return moisture, adc_val


def MoistureSensorWebserver(period=2.5):

    def uartwrite(text, delay=0.05, cipsend=True, asjson=False):
        text = text + '\r\n' if not text.endswith('\r\n') else text
        if cipsend:
            cipsend = 'AT+CIPSEND=0,' + str(len(text)) + '\r\n'
            uart.write(cipsend)
            time.sleep(delay)
            print(cipsend.strip())
        if asjson:
            text = text.replace("'", '"')
        uart.write(text)
        print(text.strip())
        time.sleep(delay)

    #Set variables
    recv=""
    recv_buf="" 
    uart = UART(1,115200) # uart on uart1 with baud of 115200
    # wifi credentials (if needed)
    wifi_ssid = ("the salami lid won't fit")
    wifi_password = ("o9#IpGMOMixU6Hkd")
    
    #Function to handle reading from the uart serial to a buffer
    def SerialRead(mode):
        SerialRecv = ""
        if mode == "0" :
            SerialRecv=str(uart.readline())
        else:
            SerialRecv=str(uart.read(mode))
        #replace generates less errors than .decode("utf-8")
        SerialRecv=SerialRecv.replace("b'", "")
        SerialRecv=SerialRecv.replace("\\r", "")
        SerialRecv=SerialRecv.replace("\\n", "\n")
        SerialRecv=SerialRecv.replace("'", "")
        return SerialRecv

    print ("Setting up Webserver...")
    time.sleep(0.1)
    print ("  - Setting Connection Mode...")
    uart.write('AT+CIPMUX=1'+'\r\n')
    time.sleep(0.75)
    print ("  - Starting Webserver..")
    uart.write('AT+CIPSERVER=1,80'+'\r\n') #Start webserver on port 80
    time.sleep(0.75)
    print ("Webserver Ready!")
    print("")

    while True:
        #read a byte from serial into the buffer
        recv=SerialRead(1)
        recv_buf=recv_buf+recv
        if '+IPD' in recv_buf: # if the buffer contains IPD(a connection), then respond
            uartwrite('HTTP/1.1 200 OK')
            uartwrite('Content-Type: application/json')
            # uartwrite('Content-Type: text/plain')
            uartwrite('Connection: close')
            uartwrite('')
            payload = read_moisture()
            uartwrite(str(payload), asjson=True)

            uartwrite('AT+CIPCLOSE=0'+'\r\n', cipsend=False) # once file sent, close connection
            recv_buf="" #reset buffer
            time.sleep(period)
        
_thread.start_new_thread(MoistureSensorWebserver(), ()) # starts the webserver in a _thread