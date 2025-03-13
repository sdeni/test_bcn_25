import threading

need_stop = False

def calc_even():
    res = 0
    while not need_stop:
        res += 2
    return res


def calc_odd():
    res = 1
    while not need_stop:
        res += 2
    return res


thread_handles = []
N = 4
for i in range(N):
    th = threading.Thread(target=calc_even if i % 2 == 0 else calc_odd)
    th.start()
    thread_handles.append(th)

while not need_stop:
    if input() == "stop":
        need_stop = True
    else:
        print("Type 'stop' to stop the threads")

for th in thread_handles:
    th.join()

print("Threads stopped")