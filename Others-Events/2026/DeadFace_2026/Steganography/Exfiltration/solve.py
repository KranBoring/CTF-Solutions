import subprocess

time_and_id = {}
times = []
for i in range(1,21):
    command = f"exiftool image_{i:02}.jpg"
    date_command = " | grep \"Date/Time Original\""
    ID_command = " | grep \"Image Unique ID\""
    res_time = subprocess.check_output(command + date_command, shell= True, text= True).split(':')
    res_ID = subprocess.check_output(command + ID_command, shell= True, text= True).split('_')
    time = int(res_time[-3][3:] + res_time[-2] + res_time[-1][:2])
    ID = bytes.fromhex(res_ID[-1][:-1])
    time_and_id = time_and_id | {time:ID}
    times.append(time)
times.sort()
flag = b""
for time in times:
    flag += time_and_id[time]
print(flag)