"""
classify.py
"""
import ast
import re

def get_clusters(f):
    clusters = []
    for line in f:
        if line.startswith('cluster'):
            line = ast.literal_eval(re.sub(r"cluster-[0-9]:","",line))
            clusters.append(line)
    return clusters
def get_names():
    male = []
    female = []
    f = open('names.txt','r')
    for line in f:
        if line.startswith('male:'):
            male = ast.literal_eval(line.replace('male:',''))
        elif line.startswith('female:'):
            female = ast.literal_eval(line.replace('female:',''))
        else:
            {}
    return male,female
    
def main():
    male_example=True
    female_example=True
    f = open('clusters.txt','r')
    clusters = get_clusters(f)
    f.close()
    male,female = get_names()
    f = open('clusters.txt','a')
    male_total_count =0
    female_total_count =0
    for index in range(len(clusters)):
        male_count = 0
        female_count =0
        unknown_count =0
        for full_name in clusters[index]:
            name = full_name.split(' ')
            #checking for first name
            if name[0] in male:
                male_count+=1
                #saving an example from each class
                if male_example is True:
                    f.write('male_class_example:'+full_name)
                    male_example=False
            elif name[0] in female:
                female_count+=1
                #saving an example from each class
                if female_example is True:
                    f.write('female_class_example:'+full_name)
                    female_example=False
            else :
                unknown_count+=1
        male_total_count+=male_count
        female_total_count+=female_count
        f.write('cluster-'+str(index)+':'+'#male:'+str(male_count)+'#female'+str(female_count)+'#unknown'+str(unknown_count)
        +'ratio male/female:'+str(male_count/female_count)+'ratio female/male:'+str(female_count/male_count))
        f.write('male_total:'+str(male_total_count)+'\n'+'female_total:'+str(female_total_count))        
    f.close()
if __name__ == '__main__':
    main()