import os
import time

import fog
import rain

path = 'Data'
raw_path = os.path.join(path, 'Raw')
fog_path = os.path.join(path, 'Fog')
if not os.path.exists(fog_path):
    os.mkdir(fog_path)
rain_path = os.path.join(path, 'Rain')
if not os.path.exists(rain_path):
    os.mkdir(rain_path)
# smoke_path = os.path.join(path, 'Smoke')

image_list = os.listdir(raw_path)

print('Detect {} files.'.format(len(image_list)))
parameter_set = [1000, 70, 34, 12, 450]
visibility_sequence = [70, 120, 225]

for i in range(len(image_list)):
    if image_list[i].startswith('.'):
        continue
    image_name = image_list[i].split('.')[0]
    image_path = raw_path + '/' + image_list[i]
    print('[{}/{}]Now processing {}.'.format(i + 1, len(image_list), image_name))
    start_time = time.time()
    # print('|_Fog simulation started.')
    # for j in range(len(visibility_sequence)):
    #     parameter_set[4] = visibility_sequence[j]
    #     fog.add_fog(image_path, image_name, fog_path, parameter_set, j)
    # print('|_Fog simulation completed.')
    print('|_Rain simulation started.')
    rain.add_rain(image_name, image_path, rain_path, 2.0)
    print('|_Rain simulation completed.')
    end_time = time.time()
    print('|_Time elapsed {}s'.format(end_time - start_time))

print('All finished!')
