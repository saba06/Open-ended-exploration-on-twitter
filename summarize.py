"""
sumarize.py
"""
def  main():
    f = open('summary.txt'+'w')
    
    fc = open('network.text','r')
    for line in fc:
        if line.startswith('Number of users collected:'):
            f.write(line)
    fc.close()
    fc. open('clusters.txt','r')
    for line in fc:
        if line.startswith('Number of communities discovered:'):
            f.write(line)
        if line.startswith('Average number of users per community:'):
            f.write(line)
        if line.startswith('Number of communities discovered:'):
            f.write(line)
        if line.startswith('male_total:' or 'female_total:'):
            f.write(line)
        if line.startswith('female_example:' or 'male_example:'):
            f.write(line)
        
    fc.close()
    f.close()
if __name__ == '__main__':
    main()