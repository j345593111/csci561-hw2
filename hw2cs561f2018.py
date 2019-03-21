import re

class applicant_information(object):
    def __init__(self, in_id, gender, age, pets, medical, car, license, days):
        self.id = in_id
        self.id_int = int(in_id)
        self.gender = gender
        self.age = age
        self.pets = pets
        self.medical = medical
        self.car = car
        self.license = license 
        self.days = days
        if(self.medical == 'N' and self.car == 'Y' and self.license == 'Y'):
            self.spla = True
        else:
            self.spla = False
        if(self.gender == 'F' and self.age >= 17 and self.pets == 'N'):
            self.lahsa = True
        else:
            self.lahsa = False
        self.picked = []
        return
    def __cmp__(self, other):
        return cmp(self.id_int, other.id_int)
    
    
    
    def output_id(self):
        print "in_id: ", self.id
        print "id_int: ", self.id_int
        print "gender: ", self.gender
        print "age: ", self.age
        print "pets: ", self.pets
        print "medical: ", self.medical
        print "car: ", self.car
        print "license: ", self.license
        print "days: ", self.days 
        print "fulfill_SPLA: ", self.spla
        print "fulfill_LAHSA: ", self.lahsa
        print "picked: ", self.picked

class organization_current(object):        
    def __init__(self, capacity, pre, ap):
        self.capacity = capacity
        self.current = {}
        self.days = [0, 0, 0, 0, 0, 0, 0]
        for i in range(len(pre)):
            self.current[pre[i][1]] = pre[i][0]
            for j in range(len(self.days)):
                self.days[j] = self.days[j] + int(ap[pre[i][0]-1].days[j])
        occupy = 0;
        for i in range(len(self.days)):
            occupy = occupy + self.days[i]
        self.efficiency = occupy
    
    def add_applicant(self, applicant):
        self.current[applicant.id] = applicant.id_int
        occupy = 0;
        for i in range(len(self.days)):
            self.days[i] = self.days[i] + int(applicant.days[i])
            occupy = occupy + int(applicant.days[i])
        self.efficiency = self.efficiency + occupy
        
    def remove_applicant(self, applicant):
        if (applicant.id in self.current):
            del self.current[applicant.id]
            occupy = 0;
            for i in range(len(self.days)):
                self.days[i] = self.days[i] - int(applicant.days[i])
                occupy = occupy + int(applicant.days[i])
            self.efficiency = self.efficiency - occupy
        else:
            print "doesn't exist"
    
    def try_applicant(self, applicant):
        for i in range(len(self.days)):
            if(int(applicant.days[i]) == 1 and self.days[i] == self.capacity):
                return False
        return True
    
    def output_current(self):
        print "capacity: ", self.capacity
        print "current: ", self.current
        print "days: ", self.days
        print "efficiency: ", self.efficiency
        
def max_value(lahsa_pool, spla_pool, lahsa_current, spla_current, ap):
    spla_pool_list = []
    for key in spla_pool:
        spla_pool_list.append(key)
    #print "spla_pool_list:", spla_pool_list
    #print "lahsa_pool:", lahsa_pool
    v = [int(-1e9), ['0']]
    for i in range(len(spla_pool_list)):
        if (spla_current.try_applicant(ap[spla_pool[spla_pool_list[i]]-1]) == True):
            #print "start"
            key = spla_pool_list[i]
            #print "key: ", key
            buffer = [] #[0] = key, [1] = value, [2] = bool(we delete from lahsa or not)
            #print "lahsa_pool:", lahsa_pool
            #print "spla_pool:", spla_pool
            #print "spla_current: "
            #spla_current.output_current()
            buffer.append(key)
            buffer.append(spla_pool[key])
            spla_current.add_applicant(ap[spla_pool[key]-1])
            del spla_pool[key]
            if key in lahsa_pool:
                buffer.append(True)
                del lahsa_pool[key]
            else:
                buffer.append(False)
            #print "before recursion\nlahsa_pool:", lahsa_pool
            #print "spla_pool:", spla_pool
            #print "spla_current: "
            #spla_current.output_current()    
            #print "buffer:", buffer    
            #recursive
            tem = min_value(lahsa_pool, spla_pool, lahsa_current, spla_current, ap)
            if (v[0] < tem[0]):
                v = tem
                v[1].append(key)
            #recursive
            spla_pool[buffer[0]] = buffer[1]
            if(buffer[2] == True):
                lahsa_pool[buffer[0]] = buffer[1]
            spla_current.remove_applicant(ap[buffer[1]-1])
            #print "after recursion\nlahsa_pool:", lahsa_pool
            #print "spla_pool:", spla_pool
            #print "spla_current: "
            #spla_current.output_current()
    if(v[0] == int(-1e9)):
        return [spla_current.efficiency, ['-1']]
    else:
        return v

def min_value(lahsa_pool, spla_pool, lahsa_current, spla_current, ap):
    lahsa_pool_list = []
    for key in lahsa_pool:
        lahsa_pool_list.append(key)
    #print "lahsa_pool_list:", lahsa_pool_list
    v = [int(1e9), ['0']]
    for i in range(len(lahsa_pool_list)):
        if (lahsa_current.try_applicant(ap[lahsa_pool[lahsa_pool_list[i]]-1]) == True):
            #print "start"
            key = lahsa_pool_list[i]
            #print "key: ", key
            buffer = [] #[0] = key, [1] = value, [2] = bool(we delete from lahsa or not)
            #print "lahsa_pool:", lahsa_pool
            #print "spla_pool:", spla_pool
            #print "lahsa_current: "
            #lahsa_current.output_current()
            buffer.append(key)
            buffer.append(lahsa_pool[key])
            lahsa_current.add_applicant(ap[lahsa_pool[key]-1])
            del lahsa_pool[key]
            if key in spla_pool:
                buffer.append(True)
                del spla_pool[key]
            else:
                buffer.append(False)
            #print "before recursion\nlahsa_pool:", lahsa_pool
            #print "spla_pool:", spla_pool
            #print "lahsa_current: "
            #lahsa_current.output_current()    
            #print "buffer:", buffer    
            #recursive
            #v = min(v, max_value(lahsa_pool, spla_pool, lahsa_current, spla_current, ap), key = lambda i : i[0])
            tem = max_value(lahsa_pool, spla_pool, lahsa_current, spla_current, ap)
            if (v[0] > tem[0]):
                v = tem
                v[1].append('*'+key)
            #recursive
            lahsa_pool[buffer[0]] = buffer[1]
            if(buffer[2] == True):
                spla_pool[buffer[0]] = buffer[1]
            lahsa_current.remove_applicant(ap[buffer[1]-1])
            #print "after recursion\nlahsa_pool:", lahsa_pool
            #print "spla_pool:", spla_pool
            #print "lahsa_current: "
            #lahsa_current.output_current()
    if (v[0] == int(1e9)):
        return max_value(lahsa_pool, spla_pool, lahsa_current, spla_current, ap)
    else:
        return v
        
def input_function():
    with open("input.txt") as fi:
        bed = int(fi.readline())
        parking = int(fi.readline())
        lahsa = int(fi.readline())
        lahsa_current = []
        for i in range(lahsa):
            in_id = fi.readline()[:5]
            exist_id = int(in_id)
            lahsa_current.append([exist_id, in_id])
        spla = int(fi.readline())
        spla_current = []
        for i in range(spla):
            in_id = fi.readline()[:5]
            exist_id = int(in_id)
            spla_current.append([exist_id, in_id])
        num = int(fi.readline())
        application_list = []
        for i in range(num):
            line = fi.readline()
            in_id = line[:5]
            gender =  line[5:6]
            age =  int(line[6:9])
            pets = line[9:10]
            medical =  line[10:11]
            car = line[11:12]
            license = line[12:13]
            days = line[13:20]
            new = applicant_information(in_id, gender, age, pets, medical, car, license, days)
            application_list.append(new)
        application_list.sort()
        return bed, parking, lahsa, lahsa_current, spla, spla_current, num, application_list

def picked(lahsa_current, spla_current, ap):
    for i in range(len(lahsa_current)):
        ap[lahsa_current[i][0]-1].picked = "LAHSA"
    for i in range(len(spla_current)):
        ap[spla_current[i][0]-1].picked = "SPLA"

def make_pool(application_list):
    spla_pool = {}
    lahsa_pool = {}
    for i in range(len(application_list)):
        if (application_list[i].spla == True and application_list[i].picked == []):
            spla_pool[application_list[i].id] = application_list[i].id_int
        if (application_list[i].lahsa == True and application_list[i].picked == []):
            lahsa_pool[application_list[i].id] = application_list[i].id_int
    return lahsa_pool, spla_pool
        
        
def check(bed, parking, lahsa, lahsa_current, spla, spla_current, num, application_list):
    print "bed: ",bed
    print "parking: ", parking
    print "lahsa: ", lahsa
    print "lahsa_current: \n", lahsa_current
    print "spla: ", spla
    print "spla_current: \n", spla_current
    print "num: ", num
    print "application_list:"
    for i in range(len(application_list)):
        application_list[i].output_id()

def check_pool(lahsa_pool, spla_pool):
    print "lahsa_pool:"
    print lahsa_pool
    print "spla_pool:"
    print spla_pool
    
def check_current(lahsa_current, spla_current):
    print "lahsa_current"
    lahsa_current.output_current()
    print "spla_current"
    spla_current.output_current()
        
bed, parking, lahsa, lahsa_pre, spla, spla_pre, num, ap = input_function()
picked(lahsa_pre, spla_pre, ap)
#check(bed, parking, lahsa, lahsa_pre, spla, spla_pre, num, ap)
lahsa_pool, spla_pool = make_pool(ap)
lahsa_current = organization_current(bed, lahsa_pre, ap)
spla_current = organization_current(parking, spla_pre, ap)
#check_current(lahsa_current, spla_current)
#check_pool(lahsa_pool, spla_pool)
output = max_value(lahsa_pool, spla_pool, lahsa_current, spla_current, ap)
#print "output: ", output
ans = output[1][len(output[1])-1]
with open("output.txt", "w") as fo:
    fo.write(ans)
#print "ans: ", ans
#print "output:", output.output_current()
#min_value(lahsa_pool, spla_pool, lahsa_current, spla_current, ap)
