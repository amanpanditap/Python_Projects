from win10toast import ToastNotifier
from playsound import playsound
import time
toaster = ToastNotifier()

#Get the required details from user
header = input("Title of reminder: ")
text = input("Message of remindar: ")
time_min=float(input("In how many minutes? "))

time_min = time_min * 60              #calculate the time in seconds

print("Setting up reminder...\n")
time.sleep(2)
print("Reminder Set!")

time.sleep(time_min)            #wait until the timer goes off

toaster.show_toast(f"{header}", f"{text}", duration=10, threaded=True)
while toaster.notification_active():
    playsound('audio.mp3')
    time.sleep(0.005)
    break
