import os
import time

import stage_gui_simple # run it actually

#r = os.system('raspivid -t 0')
#print ("return code = ", r)
exit()

# stream camera
os.chdir(os.path.abspath("/home/pi/mjpg-streamer/mjpg-streamer-experimental"))
count = 0
while 1:
	print("")
	print("")
	print("Running door camera, looping")
	print(count)
	print("")
	#r = os.system('./mjpg_streamer -i "./input_uvc.so" -o "./output_http.so"')
	r = os.system('./mjpg_streamer -i "./input_raspicam.so" -o "./output_http.so"')
	print ("return code = ", r)
	time.sleep(1)
	count += 1
