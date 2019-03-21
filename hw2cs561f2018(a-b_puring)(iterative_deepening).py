import re
import signal, os

class applicant_information(object):
    def __init__(self, in_id, gender, age, pets, medical, car, license, days):
        self.id = in_id
        self.gender = gender
        self.age = age
        self.pets = pets
        self.medical = medical
        self.car = car
        self.license = license 
        self.days = days
        self.total = 0
        for i in range(len(self.days)):
            if(self.days[i] == '1'):
                self.total = self.total + 1
        if(self.medical == 'N' and self.car == 'Y' and self.license == 'Y'):
            self.spla = True
        else:
            self.spla = False
        if(self.gender == 'F' and self.age > 17 and self.pets == 'N'):
            self.lahsa = True
        else:
            self.lahsa = False
        self.picked = []
        return      
    
    def output_id(self):
        print "in_id: ", self.id
        print "gender: ", self.gender
        print "age: ", self.age
        print "pets: ", self.pets
        print "medical: ", self.medical
        print "car: ", self.car
        print "license: ", self.license
        print "days: ", self.days 
        print "total: ", self.total
        print "fulfill_SPLA: ", self.spla
        print "fulfill_LAHSA: ", self.lahsa
        print "picked: ", self.picked

class organization_current(object):        
    def __init__(self, capacity, pre, ap):
        self.capacity = capacity
        self.days = [0, 0, 0, 0, 0, 0, 0]
        for i in range(len(pre)):
            for j in range(len(self.days)):
                self.days[j] = self.days[j] + int(ap[pre[i]].days[j])
        occupy = 0;
        for i in range(len(self.days)):
            occupy = occupy + self.days[i]
        self.efficiency = occupy
    
    def add_applicant(self, applicant):
        occupy = 0;
        for i in range(len(self.days)):
            self.days[i] = self.days[i] + int(applicant.days[i])
            occupy = occupy + int(applicant.days[i])
        self.efficiency = self.efficiency + occupy
        
    def remove_applicant(self, applicant):
        occupy = 0;
        for i in range(len(self.days)):
            self.days[i] = self.days[i] - int(applicant.days[i])
            occupy = occupy + int(applicant.days[i])
        self.efficiency = self.efficiency - occupy
    
    def try_applicant(self, applicant):
        for i in range(len(self.days)):
            if(int(applicant.days[i]) == 1 and self.days[i] == self.capacity):
                return False
        return True
    
    def output_current(self):
        print "capacity: ", self.capacity
        print "days: ", self.days
        print "efficiency: ", self.efficiency
        
def max_value(lahsa_pool, spla_pool, lahsa_current, spla_current, ap, a, b, depth):  
    #print "spla_pool_list:", spla_pool_list
    #print "lahsa_pool:", lahsa_pool
    if(depth == 0):
        return [spla_current.efficiency, ['-1']]
    depth = depth - 1
    v = [int(-1e9), ['0']]
    for i in range(len(spla_pool)):
        #print "start"
        if(stop):
            return [spla_current.efficiency, ['-1']]
        key = spla_pool[i][1]
        #print "key: ", key
        #print "lahsa_pool:", lahsa_pool
        #print "spla_pool:", spla_pool
        #print "spla_current: "
        #spla_current.output_current()
        spla_current.add_applicant(ap[key])
        buffer_lahsa_pool = []
        for j in range(len(lahsa_pool)):
            buffer_key = lahsa_pool[j][1]
            if (buffer_key != key):
                buffer_lahsa_pool.append([ap[buffer_key].total, ap[buffer_key].id])
        buffer_spla_pool = []
        for j in range(len(spla_pool)):
            buffer_key = spla_pool[j][1]
            if (spla_current.try_applicant(ap[buffer_key]) and buffer_key != key):
                buffer_spla_pool.append([ap[buffer_key].total, ap[buffer_key].id])
        #print "key: ", key
        #print "buffer_spla_pool: ", buffer_spla_pool
        #print "buffer_lahsa_pool: ", buffer_lahsa_pool
        #print "before recursion\nlahsa_pool:", lahsa_pool
        #print "spla_pool:", spla_pool
        #print "spla_current: "
        #spla_current.output_current()    
        #recursive
        tem = min_value(buffer_lahsa_pool, buffer_spla_pool, lahsa_current, spla_current, ap, a, b, depth)
        if (v[0] < tem[0]):
            v = tem
            v[1].append(key)
        elif(v[0] == tem[0] and int(v[1][len(v[1])-1]) > int(key)):
            v = tem
            v[1].append(key)    
        #recursive
        spla_current.remove_applicant(ap[key])
        #a-b puring
        if (v[0] >= b):
            return v
        a = max(a, v[0])
        #print "after recursion\nlahsa_pool:", lahsa_pool
        #print "spla_pool:", spla_pool
        #print "spla_current: "
        #spla_current.output_current()
    if(v[0] == int(-1e9)):
        return [spla_current.efficiency, ['-1']]
    else:
        return v

def min_value(lahsa_pool, spla_pool, lahsa_current, spla_current, ap, a, b, depth):
    #print "lahsa_pool_list:", lahsa_pool_list
    v = [int(1e9), ['0']]
    for i in range(len(lahsa_pool)):
        #print "start"
        key = lahsa_pool[i][1]
        #print "key: ", key
        #print "lahsa_pool:", lahsa_pool
        #print "spla_pool:", spla_pool
        #print "lahsa_current: "
        #lahsa_current.output_current()
        if(stop):
            return [spla_current.efficiency, ['-1']]
        lahsa_current.add_applicant(ap[key])
        buffer_spla_pool = []
        for j in range(len(spla_pool)):
            buffer_key = spla_pool[j][1]
            if (buffer_key != key):
                buffer_spla_pool.append([ap[buffer_key].total, ap[buffer_key].id])
        buffer_lahsa_pool = []
        for j in range(len(lahsa_pool)):
            buffer_key = lahsa_pool[j][1]
            if (lahsa_current.try_applicant(ap[buffer_key]) and buffer_key != key):
                buffer_lahsa_pool.append([ap[buffer_key].total, ap[buffer_key].id])
        #print "before recursion\nlahsa_pool:", lahsa_pool
        #print "spla_pool:", spla_pool
        #print "lahsa_current: "
        #lahsa_current.output_current()    
        #print "buffer:", buffer    
        #recursive
        #v = min(v, max_value(lahsa_pool, spla_pool, lahsa_current, spla_current, ap), key = lambda i : i[0])
        tem = max_value(buffer_lahsa_pool, buffer_spla_pool, lahsa_current, spla_current, ap, a ,b, depth)
        if (v[0] > tem[0]):
            v = tem
            v[1].append('00'+key)
        elif(v[0] == tem[0] and int(v[1][len(v[1])-1]) > int(key)):
            v = tem
            v[1].append(key)  
        #recursive
        lahsa_current.remove_applicant(ap[key])
        #a-b puring
        if(v[0] <= a):
            return v
        b = min(b, v[0])
        #print "after recursion\nlahsa_pool:", lahsa_pool
        #print "spla_pool:", spla_pool
        #print "lahsa_current: "
        #lahsa_current.output_current()
    if (v[0] == int(1e9)):
        return max_value(lahsa_pool, spla_pool, lahsa_current, spla_current, ap, a, b, depth)
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
            lahsa_current.append(in_id)
        spla = int(fi.readline())
        spla_current = []
        for i in range(spla):
            in_id = fi.readline()[:5]
            spla_current.append(in_id)
        num = int(fi.readline())
        application_list = {}
        for i in range(num):
            line = fi.readline()
            in_id = line[:5]
            gender =  line[5]
            age =  int(line[6:9])
            pets = line[9]
            medical =  line[10]
            car = line[11]
            license = line[12]
            days = line[13:20]
            new = applicant_information(in_id, gender, age, pets, medical, car, license, days)
            application_list[in_id] = new
        return bed, parking, lahsa, lahsa_current, spla, spla_current, num, application_list

def picked(lahsa_current, spla_current, ap):
    for i in range(len(lahsa_current)):
        ap[lahsa_current[i]].picked = "LAHSA"
    for i in range(len(spla_current)):
        ap[spla_current[i]].picked = "SPLA"

def make_pool(application_list, lahsa_current, spla_current):
    spla_pool = []
    lahsa_pool = []
    for key in application_list:
        if (application_list[key].spla == True and application_list[key].picked == [] and spla_current.try_applicant(application_list[key])):
            spla_pool.append([-application_list[key].total, application_list[key].id])
        if (application_list[key].lahsa == True and application_list[key].picked == [] and spla_current.try_applicant(application_list[key])):
            lahsa_pool.append([-application_list[key].total, application_list[key].id])
    spla_pool.sort()
    lahsa_pool.sort()
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
    for key in application_list:
        application_list[key].output_id()

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

def handler(signum, frame):
    global stop
    #print "cutoff"
    stop = True

stop = False    
signal.signal(signal.SIGALRM, handler)
signal.alarm(179)      
bed, parking, lahsa, lahsa_pre, spla, spla_pre, num, ap = input_function()
picked(lahsa_pre, spla_pre, ap)
#check(bed, parking, lahsa, lahsa_pre, spla, spla_pre, num, ap)
lahsa_current = organization_current(bed, lahsa_pre, ap)
spla_current = organization_current(parking, spla_pre, ap)
#check_current(lahsa_current, spla_current)
lahsa_pool, spla_pool = make_pool(ap, lahsa_current, spla_current)
#check_pool(lahsa_pool, spla_pool)
for i in range(len(spla_pool)):
    output = max_value(lahsa_pool, spla_pool, lahsa_current, spla_current, ap, -1e9, 1e9, i+1)
    #print "stop: ", stop
    #print "output: ", output
    if(stop == False):
        ans = output[1][len(output[1])-1]
        with open("output.txt", "w") as fo:
            fo.write(ans)
        #print "ans: ",ans

