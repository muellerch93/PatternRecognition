# -*- coding: utf-8 -*-
file = open("sensor_readings_24.data","r")
content = file.read()
split = content.splitlines()
categories = {
    'Move-Forward':         0,
    'Sharp-Right-Turn':     1,
    'Slight-Right-Turn':    2,
    'Slight-Left-Turn':     3
}
target_file = open('sensor_readings_mapped.data','w')
for i in range(0,len(split),1):
    features = split[i].split(",")
    category = features.pop()
    
    features.insert(0,categories[category])
    for j in range(0,len(features)-1,1):
        target_file.write("%s," % features[j])
    target_file.write("%s\n" % features[len(features)-1])
target_file.close()
