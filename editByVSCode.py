# While loop from TimeAdd is 0.01 sedond to 0.1 second
TimeAdd = 0.01
isAdded = False
while TimeAdd < 0.1:
    isAdded = False

    # Save row when time becomes larger than TimeAdd
    for index, row in df.iterrows():
        if (row['t(sec)'] > TimeAdd) & ~isAdded:
            rowAdd = row
            isAdded = True
    
    # Edit the inner value of Series
    outputStateValue = rowAdd
    outputStateValue = outputStateValue.rename(index={'t(sec)': 'TIME'})
    outputStateValue['TIME'] = 1.0
    outputStateValue = outputStateValue.rename(index={'P(atm)': 'PRES'})
    outputStateValue = outputStateValue.rename(index={'T(K)': 'TEMP'})
    
    # Convert Series to textfile (This file is used for reference only)
    name = 'inp_timeAdd' + str(TimeAdd)
    outputStateValue.to_csv(name, sep=' ', header=False, float_format='%g' )
    
    # Open the keyword inpfile used in SENKIN
    name_output = 'inp_key_timeAdd' + str(TimeAdd)
    outputFile = open(name_output, "w")
    outputFile.write("CONP\n")
    
    # Convert the textfile to inpfile
    with open(name, 'r') as f:
        for line in f:
            if "TIME" in line: 
                outputFile.write(line)
                outputFile.write("DELT 1.0E-12\n")
            elif "PRES" in line: outputFile.write(line)
            elif "TEMP" in line: outputFile.write(line)
            else:                outputFile.write("REAC " + line)
    outputFile.write("END\n")
    outputFile.close()

    # Update TimeAdd
    TimeAdd = TimeAdd + 0.01