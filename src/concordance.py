import re

    
def get_context(text, start, end):
    cdistance = 10
    if ((start - cdistance) > 0) and ((end + cdistance) < len(text)):
        return text[(start - cdistance):(end + cdistance)]
    elif ((start -cdistance) > 0) and ((end + cdistance) > len(text)):
        #this is outside the text's range...
        return ""
    elif (start - cdistance) < 0:
        if (end + cdistance) > len(text):
            return text[0:len(text)]
        else:
            return text[0:(end + cdistance)]
    elif (end + cdistance) > len(text):
        if (start - cdistance) < 0:
            return text[0: len(text)]
        else:
            return text[(start - cdistance): len(text)]
    else:
        #any other case that's not covered - simply don't return anything
        return ""
        
    
print "start"

#http://cs.brown.edu/courses/cs0931/2012/assignments/HW2-4/HW2-4.pdf

#print get_word("His name is Charles, Prince of Wales, the heir apparent.", 13)  # 'Earl'
#print get_word("Hello, my name is Earl.", 20) 

print get_context("His name is Charles the heir apparent.", 6, 19)  # 'Earl'
print get_context("His name is Charles the heir apparent.", 35, 37)  # 'Earl'


print "end"