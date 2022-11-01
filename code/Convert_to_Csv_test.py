import struct
import datetime
import csv

# load the dataset
class BinaryReaderEOFException(Exception):
    def __init__(self):
        pass
    def __str__(self):
        return 'Not enough bytes in file to satisfy read request'

class BinaryReader:
    # Map well-known type names into struct format characters.
    typeNames = {
        'int8'   :'b',
        'uint8'  :'B',
        'int16'  :'h',
        'uint16' :'H',
        'int32'  :'i',
        'uint32' :'I',
        'int64'  :'q',
        'uint64' :'Q',
        'float'  :'f',
        'double' :'d',

        'char'   :'s'}

    def __init__(self, fileName):
        self.file = open(fileName, 'rb')

    def read(self, typeName):
        typeFormat = BinaryReader.typeNames[typeName.lower()]
        typeSize = struct.calcsize(typeFormat)
        value = self.file.read(typeSize)
        if typeSize != len(value):
            raise BinaryReaderEOFException
        return struct.unpack(typeFormat, value)[0]

    def __del__(self):
        self.file.close()

def readbinfile(filename):
    binaryReader = BinaryReader(filename)

    row=[]
    counter=0
    try:
        file_csv = open("FlyerZz2_Dsr_test.csv", "w")
        # packetId = binaryReader.read('uint8')
       # timestamp = binaryReader.read('int32')
       # with open('largeee.csv', 'w') as f12:
            #columnTitleRow = "GT, F1,F2,TTick,Time\n"
           # f12.write(columnTitleRow)

        while (counter<800):
                f1 = (binaryReader.read('double'))
                #print(f1)
                f2 = (binaryReader.read('double'))
                #print(f2)
                f3 = (binaryReader.read('double'))
                #print(f3)
                f4 = (binaryReader.read('uint64'))
                #print(f4)
                if (f4 == ''):
                    break
                secs = int(f4 / 10000000)
                #print(secs)
                delta =datetime.timedelta(seconds=secs)
                datetime.timedelta(733940, 34260)
                ts = datetime.datetime(1,1,1) + delta
                #print(ts)
                fmt = '%Y/%m/%d-%H:%M:%S.%d'
                now_str = ts.strftime(fmt)
                if (f1<=0.35999):
                    f1=2
                elif(0.36<f1<=0.65999):
                    f1=3
                elif(0.66<f1<=1):
                    f1=1

                row.append(str(f1) + "," + str(f2)+"," + str(f3)+ "," + str(f4) +"," + now_str +"\n")
                counter=counter+1
                print(row)
                file_csv.write(str(f1) + "," + str(f2) + "," + str(f3) + "," + str(f4) + "," + now_str + "\n")

        return row,counter
# rowsc=[]
# rowsc,conter=readbinfile('FlyerEu_Tp70_MinSp20_4h_Dsr.bin')
# print(rowsc[1],conter)
    except BinaryReaderEOFException:
        # One of our attempts to read a field went beyond the end of the file.
        print ("Error: File corrupted.")

res=BinaryReader('FlyerZz2_Tp7_MinSp2_Dsr.bin')
res.read('double')
readbinfile('FlyerZz2_Tp7_MinSp2_Dsr.bin')