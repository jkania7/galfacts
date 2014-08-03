
ver = "v1.0.0"

def main():
    print("Converter {0}".format(ver))

    pad = float(raw_input("Please enter the amount of padding you" +\
                          " would like (in arc min): "))
    pad = pad/(60)
    
    RA_start = parser(raw_input("Please enter start RA: "))
    RA_stop = parser(raw_input("Please enter stop RA: "))
    RA_start_deci = RA_to_decimal(RA_start) + pad
    RA_stop_deci = RA_to_decimal(RA_stop) - pad

    DEC_start = parser(raw_input("Please enter start DEC: "))
    DEC_stop = parser(raw_input("Please enter stop DEC: "))
    DEC_start_deci = DEC_to_decimal(DEC_start) + pad
    DEC_stop_deci = DEC_to_decimal(DEC_stop) - pad

    print("---------")
    print("RA start in decimal = {0:.2f}".format(RA_start_deci))
    print("RA stop in decimal = {0:.2f}".format(RA_stop_deci))
    print("DEC start in decimal = {0:.2f}".format(DEC_start_deci))
    print("DEC stop in decimal = {0:.2f}".format(DEC_stop_deci))

def parser(str):
    result = []
    for i in range(len(str)):
        result.append(float(str[i]))
    if len(result) != 6:
        print("You did not enter the correct lenght")
    return result

def RA_to_decimal(RA):
    hour_deci = (10*RA[0]+RA[1]) + (10*RA[2]+RA[3])/60 + (10*RA[4]+RA[5])/(60*60)
    RA_deg_deci = hour_deci*15
    return RA_deg_deci

def DEC_to_decimal(DEC):
    DEC_deci = (10*DEC[0]+DEC[1]) + (10*DEC[2]+DEC[3])/60 + (10*DEC[4]+DEC[5])/(60*60)
    return DEC_deci

if __name__ == "__main__":
    main()
