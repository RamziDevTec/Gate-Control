import serial
import time

def gate(alarm_off = False, alarm_on = False,  door_close = False, door_open = False):
    # Variablen auf Standard zurücksetzen
    SOI     = 0xAA   # Start of Information, immer AA
    RES     = 0x00   # Reserved, Standard 00
    ADR_S   = 0x01   # Source Address, Standard PC/Software = 01
    CID1    = 0x00   # Control Character 1, Standard 00
    CID2    = 0x00   # Control Character 2, Standard 00
    ADR_T   = 0x00   # Target Address, Standard Gate-Adresse 01
    DLC     = 0x08   # Data Length, Standard 8 Byte
    DATA0   = 0x00
    DATA1   = 0x00
    DATA2   = 0x00
    DATA3   = 0x00
    DATA4   = 0x00
    DATA5   = 0x00
    DATA6   = 0x00
    DATA7   = 0x00
    CHK     = 0x10   # Prüfsumme, wird automatisch berechnet

    # Packet jenach Aktion konfigurieren
    if alarm_off:
        CID1 = 0x02
        DATA0 = 0x02
    elif alarm_on:
        CID1 = 0x02
        DATA0 = 0x02
        DATA1 = 0x01
    elif door_close:
        CID1 = 0x02
        DATA1 = 0x02
    elif door_open:
        CID1 = 0x02
    else:
        return "===== KEINE AKTION ERKANNT ====="

    # Packet vollständigen
    packet = [SOI, RES, ADR_S, CID1, CID2, ADR_T, DLC,
          DATA0, DATA1, DATA2, DATA3, DATA4, DATA5, DATA6, DATA7, CHK]
    CHK = sum(packet[1:15]) & 0xFF
    packet[15] = CHK

    # Packet senden und Verbindung trennen
    ser.write(packet)
    ser.close()


# RS485-Port öffnen
ser = serial.Serial(
    port='COM4',          # euer Adapter
    baudrate=9600,        # falls nicht korrekt: ausprobieren 19200, 38400 etc.
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)


gate(door_open=True)
time.sleep(5)
gate(door_close=True)
