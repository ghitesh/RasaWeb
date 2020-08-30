import re
str='''TCS iON Digital Exam Management combines the accuracy of technology with the expertise of professional evaluators to give a complete examination solution to academic institutions. Here are some key benefits. For more info: http://bit.ly/TCSiON_ContactUs #TCSiON #digital #solutions
TCS iON Digital Exam Management automates the entire exam process, speeds and scales up the #operations while maintaining #security and transparency. For more information, contact us on: http://bit.ly/TCSiON_ContactUs #TCSiON #exam #Management #Digital #solution"
Read how TCS iON is preparing students to become the nation builders of the future by equipping them with skills beyond academics. Visit: http://bit.ly/3a3aLuH #TCSiON #IntelliGem #GemsofTomorrow #Skills #GenZ
'''

print(str)
str1 = re.sub("http.+[ ]","",str)
print(str1)
str1 = re.sub("[\.,\":]","", str1)


print(str1)
#str1 = " ".join(str1)
print(str1)
str1 = re.sub("(^| )[a-zA-Z]{,2}(?= )","",str1)
print(str1)

str1 = re.sub("(^| )[a-zA-Z]*[0-9][a-zA-Z0-9]*","", str1)
print(str1)
