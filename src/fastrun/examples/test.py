import time

print("fastrun test started", flush=True)

for second in range(1, 6):
    print(f"fastrun test: second {second}/5", flush=True)
    time.sleep(1)

print("fastrun test finished", flush=True)
