import os
import matlab
import matlab.engine

import fog


def add_rain(image_name, image_path, rain_path, alpha):
    parameter_set = [1000, 70, 34, 12, 500]
    fog.add_fog(image_path, image_name, rain_path, parameter_set, 100)
    image_name += '_rain'
    image_path = os.path.join(rain_path, image_name + '.jpg')
    print(' |_Fog mask added.')
    engine = matlab.engine.start_matlab()
    print(' |_MATLAB engine started.')
    engine.add_rain(image_path, image_name, rain_path, matlab.double(alpha), nargout=0)
    engine.exit()

