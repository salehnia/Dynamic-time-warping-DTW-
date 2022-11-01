import struct
import datetime
import numpy as np
import csv

# load the dataset
class BinaryReaderEOFException(Exception):
    def __init__(self):
        pass
    def __str__(self):
        return 'Not Enough Info In File...'

class BinaryReader:
    # Map well-known type names into struct format characters.
    typeNames = {
        # 'int8'   :'b',
        # 'uint8'  :'B',
        # 'int16'  :'h',
        # 'uint16' :'H',
        # 'int32'  :'i',
        # 'uint32' :'I',
        # 'int64'  :'q',
        'uint64' :'Q',
        # 'float'  :'f',
        'double' :'d'
        # 'char'   :'s'
    }

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

def binfile_operation(filename):
    # binaryReader = BinaryReader('FlyerZz1_Tp7_MinSp2_TrainDs_ByQ_T1a.bin')
    binaryReader = BinaryReader(filename)
    # length_All = binaryReader.read('uint64').count()
    # print(length_All)
    row=[]
    row_final_csv=[]
     # counting classes  0.65<grand_t<=1
    try:
        # packetId = binaryReader.read('uint8')
       # timestamp = binaryReader.read('int32')
       # with open('largeee.csv', 'w') as grand_t2:
            #columnTitleRow = "GT, grand_t,sensor1,TTick,Time\n"
           # grand_t2.write(columnTitleRow)
        csv2 = open("FlyerEu_Tp70_MinSp20_334d_Dsr.csv", "w")
        csv_final = open("final_DB_as.csv", "w")
        for i in range(25,40000,25):
            grand_t_final = 0
            grand_t_sum = 0
            sensor1_sum = 0
            sensor1_final = 0
            sensor2_sum = 0
            sensor2_final = 0
            time_sum = 0
            time_final = 0
            # grand_t_count2 = 0  # counting classes grand_t<=0.35
            # grand_t_count3 = 0  # counting classes  0.65<grand_t<=1
            # grand_t_count1 = 0
            date_median = np.array([],dtype=str)
            counter = i - 25
            while(counter < i + 25):
                grand_t = (binaryReader.read('double'))
                #print(grand_t)
                sensor1 = (binaryReader.read('double'))
                sensor1_sum = sensor1_sum + sensor1
                #print(sensor1)
                sensor2 = (binaryReader.read('double'))
                sensor2_sum = sensor2_sum + sensor2
                #print(sensor2)
                time = (binaryReader.read('uint64'))
                time_sum = time_sum + time
                #print(time)
                if (time == ''):
                    break
                secs = int(time / 10.0 ** 7)
                #print(secs)
                delta =datetime.timedelta(seconds=secs)
                datetime.timedelta(733940, 34260)
                ts = datetime.datetime(1,1,1) + delta
                #print(ts)
                fmt = '%Y/%m/%d-%H:%M:%S.%d'
                now_str = ts.strftime(fmt)
                date_median = np.append(date_median,now_str)
                # print(time)
                if (grand_t<=0.35999):
                    grand_t=2
                    # grand_t_count2 = grand_t_count2 + 1
                elif(0.36<grand_t<=0.65999):
                    grand_t=3
                    #grand_t_count3 = grand_t_count3 + 1
                elif(0.66<grand_t<=1):
                    grand_t=1
                    #grand_t_count1 = grand_t_count1 + 1
                row.append(str(grand_t) + "," + str(sensor1)+"," + str(sensor2)+ "," + str(time) +"," + now_str +"\n")
                counter=counter+1
                # grand_t_sum += grand_t
                print(row)
                # print(time)
                csv2.write(str(grand_t) + "," + str(sensor1)+"," + str(sensor2)+ "," + str(time) +"," + now_str +"\n")
                grand_t_final = grand_t
            # if (grand_t_max == grand_t_count1):
            #     grand_t_final = 1
            # if (grand_t_max == grand_t_count2):
            #     grand_t_final = 2
            # if (grand_t_max == grand_t_count3):
            #     grand_t_final = 3
            sensor1_final = sensor1_sum / 50
            sensor2_final = sensor2_sum / 50
            time_final = time_sum / 50
            row_final_csv.append(str(grand_t_final) + "," + str(sensor1_final)+"," + str(sensor2_final)+ "," + str(time_final) +"," + date_median[25] +"\n")
            csv_final.write(str(grand_t_final) + "," + str(sensor1_final)+"," + str(sensor2_final)+ "," + str(time_final) +"," + date_median[25] +"\n")
        return row

    except BinaryReaderEOFException:
        # One of our attempts to read a field went beyond the end of the file.
        print ("Error: File seems to be corrupted.")

# rowsc=[]
# rowsc,conter=binfile_operation('FlyerEu_Tp70_MinSp20_4h_Dsr.bin')
# print(rowsc[1],conter)

b3=BinaryReader('FlyerEu_Tp70_MinSp20_334d_Dsr.bin')
b3.read('double')
binfile_operation('FlyerEu_Tp70_MinSp20_334d_Dsr.bin')
print('done')