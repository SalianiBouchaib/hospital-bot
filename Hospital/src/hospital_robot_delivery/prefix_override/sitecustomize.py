import sys
if sys.prefix == '/usr':
    sys.real_prefix = sys.prefix
    sys.prefix = sys.exec_prefix = '/mnt/c/Users/MSI/Desktop/project robotv2 prime-trial/project robotv2/hospital_robot_ws/install/hospital_robot_delivery'
