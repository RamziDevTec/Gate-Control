import serial
import time

# Standardwerte für 16-Byte-Datenpaket der Gate-Platine

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

# Paket als Liste zusammenbauen
packet = [SOI, RES, ADR_S, CID1, CID2, ADR_T, DLC,
          DATA0, DATA1, DATA2, DATA3, DATA4, DATA5, DATA6, DATA7, CHK]

# Prüfsumme berechnen
def calc_checksum(pkt):
    return sum(pkt[1:15]) & 0xFF

def set_packet(SOI=0xAA, RES = 0x00, ADR_S = 0x01, CID1 = 0x00, CID2 = 0x00, ADR_T = 0x00, DLC = 0x08, DATA0 = 0x00, DATA1 = 0x00, DATA2 = 0x00, DATA3 = 0x00, DATA4 = 0x00, DATA5 = 0x00, DATA6 = 0x00, DATA7 = 0x00, CHK = 0x10):
    global packet
    packet = [SOI, RES, ADR_S, CID1, CID2, ADR_T, DLC,
          DATA0, DATA1, DATA2, DATA3, DATA4, DATA5, DATA6, DATA7, CHK]
    CHK = sum(packet[1:15]) & 0xFF
    packet[15] = CHK

# RS485-Port öffnen
ser = serial.Serial(
    port='COM3',          # euer Adapter
    baudrate=9600,        # falls nicht korrekt: ausprobieren 19200, 38400 etc.
    parity=serial.PARITY_NONE,
    stopbits=serial.STOPBITS_ONE,
    bytesize=serial.EIGHTBITS,
    timeout=1
)

# Testen
set_packet(CID1=0x02, DATA0=0x02, DATA1=0x01)

ser.write(packet)
print("Befehl gesendet:", packet)


# Verbindung schließen
ser.close()
