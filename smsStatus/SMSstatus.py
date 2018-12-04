def main():
    # this program opens report file and extracts guardian id, 
    # phone number and opt-in status
    
    content = get_content("report.csv")
    gards = get_gua(content)
    info = make_lists(gards)
    extract(info)
    
def get_content(filename):
    # filename is the name of the report file
    # open report, read contents and place each
    # line of the file as a list entry in contents list
    
    file = open(filename,"r")
    content = file.read().splitlines()
    file.close()
    return content  

def get_gua(content):
    # content is a list of lines from report file
    # removes quotes
    # checks for 'gua' prefix and append relevant lines to gards list
    
    gards  = []
    
    for line in content:
        line = line.replace('"','')
        if line[:3] == "gua":
            gards.append(line)
            
    return gards

def make_lists(gards):
    # gards is a list of all lines from report starting with 'gua'
    # transforms each line from report and splits on commas and stores
    # in a new nested
    
    info = []
    
    for line in gards:
        line_info = line.split(',')
        info.append(line_info)

    return info
    
def extract(info):
    # info is a nested list of guardian info
    # creates a new file and writes all guardian ids,
    # phone numbers and opt-in status
    
    newfile = open("output.txt","w")
    
    for line in info:
        newfile.write("id: {0}, phone number: {1}, status: {2}\n".format(line[0][5:],line[3],line[4]))
    
    newfile.close

main()