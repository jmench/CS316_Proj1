#!/usr/bin/python

# Author: Jordan Menchen

import cgi
import cgitb
import subprocess

# Creating a multi-dimensional array
# Ordered as ["key", "convert to", conversion value]
conversionTable = [
    ["usdollar", "euro", 0.88],
    ["usdollar", "xarn", 26.2],
    ["usdollar", "icekrona", 119.88],
    ["xarn", "polandzloty", 0.1434198],
    ["icekrona", "galacticrock", 0.001029839],
    ["parsec", "lightyear", 3.26],
    ["lightyear", "kilometer", 95000000000000],
    ["lightyear", "mile", 5886000000000],
    ["xlarn", "parsec", 7.3672],
    ["galacticyear", "terrestrialyear", 250000000],
    ["xarnyear", "terrestrialyear", 1.2579],
    ["terrestrialyear", "terrestrialminute", 525600],
    ["bar", "kilopascal", 100],
    ["torr", "kilopascal", 0.1333223684211],
    ["psi", "torr", 51.71487786825],
    ["hour", "second", 3600],
    ["day", "hour", 24],
    ["hour", "minute", 60]
]

# Function to clean up repeated HTML code
def startHTML():
    print ("<html>")
    print ("<head>")
    print ("<style>")
    print ("table, td, th {border: 3px solid grey; text-align: center;}")
    print ("table {width: 600; border-collapse: collapse;}")
    print ("th {font-size: 22px; background-color: #1D1B1B; color: #EC4D37;}")
    print ("td {text-align: center;}")
    print ("</style>")
    print ("</head>")
    print ("<body bgcolor = \"lightgray\">")
    print ("<table cellspacing=\"20\">")

# Function that simply checks if the value is in the conversion table
def isValInTable(val):
    for conversion in conversionTable:
        if (conversion[0] == val or conversion[1] == val):
            return True
    return False

# Function that checks if the input is a valid number
def validateNum(num):
    try:
        float(num)
        return True
    except ValueError:
        return False

# Function that checks if there is any input
def checkValForNone(val):
    if (val == None):
        return "missing"
    else:
        return val.lower()

# Function that checks if there is a one step path between maybein and maybeout
def ispath(maybein, maybeout):
    # Loop through every conversion in the table
    for conversion in conversionTable:
        # Check if maybein and maybeout are the same
        if((conversion[0] == maybein and conversion[1] == maybeout) or
                (conversion[1] == maybein and conversion[0] == maybeout)):
            return ("DIRECTPATH")
        # Else check if the first index is equal to maybein
        elif (conversion[0] == maybein):
            # If it is, set the second index as the possible path
            possiblePath = conversion[1]
            # Loop through the conversions again
            for paths in conversionTable:
                # Check if the conversion has a path from possiblePath to
                # maybeout
                if (paths[0] == possiblePath and paths[1] == maybeout):
                    return (possiblePath)
        # Same as above, just checking in reverse
        elif (conversion[1] == maybein):
            possiblePath = conversion[0]
            for paths in conversionTable:
                if (paths[1] == possiblePath and paths[0] == maybeout):
                    return (possiblePath)
    # If there is no path, return "NOPATH"
    return ("NOPATH")

# Function to check if the input to the form is valid
def isPart2Valid(maybein, maybeout):
    if (maybein == "missing" or not(isValInTable(maybein))):
        return False
    elif (maybeout == "missing" or not(isValInTable(maybeout))):
        return False
    else:
        return True

# This is the function for part 2 - is path?
def part2(form):
    # This is where the HTML begins for part 2
    startHTML()
    print ("<tr>")
    print ("<th>MAYBEIN</th>")
    print ("<th>MAYBEOUT</th>")
    print ("<th>ANSWER / NOPATH</th>")
    print ("</tr>")
    print ("<tr>")

    # Get the form input and check if they are None
    # Sets the value to "missing" if it is None
    maybein = checkValForNone((form.getvalue('maybein')))
    maybeout = checkValForNone((form.getvalue('maybeout')))
    path = None

    # Check the values from above and print them in the table accordingly
    # Error checks if the value is missing or does not exist in the table
    if (maybein == "missing"):
        print ("<td><font color = \"red\">"), maybein, ("</font></td>")
        path = "maybein missing"
    elif (not(isValInTable(maybein))):
        print ("<td><font color = \"blue\">"), maybein, ("</font></td>")
        path = "unknown choice"
    else:
        print ("<td>"), maybein, ("</td>")

    if (maybeout == "missing"):
        print ("<td><font color = \"red\">"), maybeout, ("</font></td>")
        path = "maybeout missing"
    elif (not(isValInTable(maybeout))):
        print ("<td><font color = \"blue\">"), maybeout, ("</font></td>")
        path = "unknown choice"
    else:
        print ("<td>"), maybeout, ("</td>")

    # Checks if the form is valid and checks for a path if so
    if (isPart2Valid(maybein, maybeout)):
        path = ispath(maybein, maybeout)

    if (path == "NOPATH"):
        print ("<td><font color = \"red\">"), path, ("</font></td>")
    else:
        print ("<td><font color = \"green\">"), path, ("</font></td>")
    print ("</tr>")
    print ("</table>")
    print ("</body>")
    print ("</html>")

# Function that converts a value of myin to myout
def convert(myin, myout, inamount):
    # Check if myin and myout are the same - no conversion needed if so
    if (myin == myout):
        return inamount
    else:
        # Loop through the conversions
        for conversion in conversionTable:
            # Check if the first index equals the myin value
            if (conversion[0] == myin):
                # Check if the second index equals the myout value
                if(conversion[1] == myout):
                    # Conversion found - return converted amount
                    return (float(inamount) * conversion[2])
            # Same process as above just in reverse
            elif (conversion[1] == myin):
                if(conversion[0] == myout):
                    # Divide here b/c the conversion is bi-directional
                    return (float(inamount) / conversion[2])
    # If no conversion is found, return None
    return None

# Function to check if the input to the form is valid
def isPart1Valid(myin, myout, inamount):
    if (myin == "missing" or not(isValInTable(myin))):
        return False
    elif (myout == "missing" or not(isValInTable(myout))):
        return False
    elif (inamount == "missing" or not(validateNum(inamount))):
        return False
    else:
        return True

# This is the function for part 1 - the conversion
def part1(form):
    # This is where the HTML begins for part 1
    startHTML()
    print ("<tr>")
    print ("<th colspan = 5> Part 1 - Conversion </th>")
    print ("</tr>")
    print ("<tr>")
    print ("<th>IN</th>")
    print ("<th>OUT</th>")
    print ("<th>QUANTITY</th>")
    print ("<th></th>")
    print ("<th>ANSWER/ERROR</th>")
    print ("</tr>")
    print ("<tr>")

    # Gets the values in the form and checks if they are None
    # Sets the value to "missing" if it is None
    myin = checkValForNone((form.getvalue('myin')))
    myout = checkValForNone((form.getvalue('myout')))
    inamount = checkValForNone((form.getvalue('inamount')))
    outamount = None

    # Check the values from above and print them in the table accordingly
    # Error checks if the value is missing or does not exist in the table
    if (myin == "missing"):
        print ("<td><font color = \"red\">"), myin, ("</font></td>")
        outamount = "myin missing"
    elif (not(isValInTable(myin))):
        print ("<td><font color = \"blue\">"), myin, ("</font></td>")
        outamount = "unknown choice"
    else:
        print ("<td>"), myin, ("</td>")

    if (myout == "missing"):
        print ("<td><font color = \"red\">"), myout, ("</font></td>")
        outamount = "myout missing"
    elif (not(isValInTable(myout))):
        print ("<td><font color = \"blue\">"), myout, ("</font></td>")
        outamount = "unknown choice"
    else:
        print ("<td>"), myout, ("</td>")

    if (inamount == "missing"):
        print ("<td><font color = \"red\">"), inamount, ("</font></td>")
        outamount = "inamount missing"
    elif (not(validateNum(inamount))):
        print ("<td><font color = \"green\">"), inamount, ("</font></td>")
        outamount = "invalid amount"
    else:
        print ("<td>"), inamount, ("</td>")

    # Checks if the form is valid and runs the conversion if so
    if (isPart1Valid(myin, myout, inamount)):
        outamount = convert(myin, myout, inamount)

    print ("<td>--</td>")
    print ("<td>"), outamount, ("</td>")
    print ("</tr>")
    print ("</table>")
    print ("</body>")
    print ("</html>")

# This error checks for an empty form and outputs the first table as specified
# if the form is empty.
def checkEmptyForm(form):
    if ((form.getvalue('myin')) == None and (form.getvalue('myout')) == None
            and (form.getvalue('inamount')) == None and (form.getvalue('maybein')) == None
            and (form.getvalue('maybeout')) == None):
        startHTML()
        print ("<tr>")
        print ("<th>IN</th>")
        print ("<th>OUT</th>")
        print ("<th>QUANTITY</th>")
        print ("<th>         </th>")
        print ("<th>ANSWER/ERROR</th>")
        print ("</tr>")
        print ("<tr>")
        print ("<td id=\"myin\"> -- </td>")
        print ("<td id=\"myout\"> -- </td>")
        print ("<td id=\"inamount\"> -- </td>")
        print ("<td></td>")
        print ("<td id=\"outamount\"> Nothing submitted, nothing returned.</td>")
        print ("</tr>")
        print ("</table>")
        print ("</body>")
        print ("</html>")
        return True
    return False

def main():
    cgitb.enable()
    print "Content-type: text/html\n"
    form = cgi.FieldStorage()
    if (checkEmptyForm(form)):
        exit()
    else:
        if ((form.getvalue('submit2')) == None):
            part1(form)
        elif ((form.getvalue('submit1')) == None):
            part2(form)
        else:
            print("<html>")
            print("<body>")
            print("<h1> Please use only one submit button. </h1>")
            print("</body>")
            print("</html>")

if __name__ == "__main__":
    main()
