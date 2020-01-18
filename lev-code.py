import random
import copy
import multiprocessing

def minimumEditDistance(s1,s2):
    if len(s1) > len(s2):
        s1,s2 = s2,s1
    distances = range(len(s1) + 1)
    for index2,char2 in enumerate(s2):
        newDistances = [index2+1]
        for index1,char1 in enumerate(s1):
            if char1 == char2:
                newDistances.append(distances[index1])
            else:
                newDistances.append(1 + min((distances[index1],
                                             distances[index1+1],
                                             newDistances[-1])))
        distances = newDistances
    return distances[-1]
 
alphabet = ["0", "1", "2", "3"]

def all_codes():
    code = set()
    for a in alphabet:
        for b in alphabet:
            for c in alphabet:
                for d in alphabet:
                    for e in alphabet:
                        for f in alphabet:
                            code.add(a+b+c+d+e+f)
    return list(code)

def get_two_random(all_codes):
    codes = copy.deepcopy(all_codes)
    codes = all_codes
    random.shuffle(codes)
    one = random.choice(codes)
    two = ""
    three = ""
    for code in codes:
        if minimumEditDistance(one, code) >= 3:
            two = code
            break
    for code in codes:
        if minimumEditDistance(one, code) >= 3 and minimumEditDistance(two, code) >= 3:
            three = code
            break
    return [one, two, three]

def build(all_codes):
   # good_codes = get_two_random(all_codes)
    good_codes = ["230013", "110321", "220022"]
    for code in all_codes:
        far = True
        for good in good_codes:
            if minimumEditDistance(code, good) < 3:
                far = False
                break
        if far:
            good_codes.append(code)    
    return good_codes    

def heuristic(results):
    best_len = 0
    best_codes = []
    for i in range(1):
        codes = build(all_codes()) 
        if len(codes) > best_len:
            best_len = len(codes)
            best_codes = codes
        print(i, best_len, len(codes))
    results.append([best_codes, best_len])

def aggregate_processes(results):
    best_code = []
    best_len = 0
    for result in results:
        if result[1] > best_len:
            best_len = result[1]
            best_code = result[0]
    return best_code, best_len

if __name__ == '__main__':
    manager = multiprocessing.Manager()
    results = manager.list()
    jobs = []
    for i in range(8):
        p = multiprocessing.Process(target=heuristic, args=(results, ))
        jobs.append(p)
        p.start()

    for proc in jobs:
        proc.join()

    code, length = aggregate_processes(results)
    with open('codebook.txt', 'w') as codebook:
        codebook.write(str(code))

    print(code, length)

