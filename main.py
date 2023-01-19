import re

inter_file = open("Intermediate_code.txt","a")
inter_file.truncate(0)
inter_file.close()

begin_re = re.compile("^MACRO.*$")
end_re = re.compile("^MEND.*$")
should_write = True

with open("Sample_1.asm") as input_fh:
    with open("Intermediate_code.txt", "w", encoding="UTF-8") as output_fh:
        for line in input_fh:
            line = line.strip()

            if begin_re.match(line):
                should_write = False
            if should_write:
                print(line, file=output_fh)
            if end_re.match(line):
                should_write = True
inter_file.close()

code_file = open("Sample_1.asm ","r")
MDT_file = open("MDT.txt","a+")
MDT_file.truncate(0)
MDT_file.close()

MNT_file = open("MNT.txt","a+")
MNT_file.truncate(0)
MNT_file.close()

lines = code_file.readlines()
mntc = 1
mdtc = 0
alac = 0
a=0

mnt  = []
ala = []
mdt = []
exp_macro = []
prev = ""

flag = 0
for line in lines:
    line = line.replace("\n","")
    sp = line.split()
    if prev =="MACRO" and flag == 1:
        mnt.append([sp[0],mdtc,len(sp[1:])])
        inc = 0
        for arg in sp[1:]:
            sa =  arg.split("=")
            inc += 1
            if len(sa) == 2:
                sa_1 = sa[0].split(",")
                ala.append([alac,mntc,inc,sa_1[0],sa[1],sp[0]])
            else:
                sa_2 = arg.split(",")
                ala.append([alac,mntc,inc,sa_2[0],sp[0]]) 
            alac += 1
        mntc += 1
    if sp[0].upper() == "MACRO":
        prev = sp[0].upper()
        flag = 1
    elif flag == 1:
        m_name = sp[0]
        mdtc +=1
        flag = 2
    elif flag == 2:
        word = line.split()
        if len(word) > 1:    
            found = False
            for i in ala:
                if word[1] == i[3] and m_name == i[4]:
                    exp_macro.append([m_name,word[0],"#"])
                    mdt.append(str(word[0]+"\t#"+str(i[2])))
                    found=True
                    break
            if found == False:
                exp_macro.append([m_name,word[0],word[1]])
                mdt.append(line)
        else:
            if line != "MEND": 
                exp_macro.append([m_name,word[0]])
            mdt.append(line)
        mdtc += 1
        if sp[0].upper() == "MEND":
            flag = 0

e_i = 0
for exp in exp_macro:
    for exp_1 in exp_macro:
        if exp[1] == exp_1[0]:
            exp_macro.pop(e_i)
            if len(exp_1)>2:
                exp_macro.append([exp[0],exp_1[1],exp_1[2]])
            else:
                exp_macro.append([exp[0],exp_1[1]])
    e_i += 1

mdt_copy = []
act = []
i = 1
for M in mdt:
   #print(M)
   ln = M.split()
   found = False
   for exp in exp_macro:
       if ln[0] == exp[0]:
           found = True
           if len(exp) > 2:
               if exp[2] == "#":
                   mdt_copy.append(str(exp[1])+"\t"+str(ln[1]))
                   #print(ln[0])
                   act.append([ln[1],i,ln[0]])
                   i += 1
               else:
                   mdt_copy.append(str(exp[1])+"\t"+str(exp[2]))
           else:
               mdt_copy.append(str(exp[1]))
   if found == False:
       mdt_copy.append(str(M))     

MNT_file = open("MNT.txt","w")
MDT_file = open("MDT.txt","w")
f_p = open("formal_vs_positional.txt","w") 
a_p = open("actual_vs_positional.txt","w")
#print ("\n argument list table")
for arg in ala: 
    #print (arg)
    f_p.write(str(arg[3])+"\t\t#"+str(arg[2])+"\t\t"+str(arg[4])+"\n")
f_p.close()

for a in act:
    #print(a)
    a_p.write(str(a[0])+"\t\t#"+str(1)+"\t\t"+str(a[2])+"\n")
a_p.close()

for m in mnt:
    #print (m) 
    MNT_file.write(str(m[0])+"\t\t"+str(m[1])+"\t\t"+str(m[2])+"\n")
MNT_file.close()

for l in mdt_copy: 
    MDT_file.write(str(l))
    MDT_file.write("\n")
MDT_file.close()
