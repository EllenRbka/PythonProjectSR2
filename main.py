import time
import random
import threading


class PhysicalClock:
    def __init__(self, process_id):
        self.process_id = process_id
        self.time = 0
        self.lock = threading.Lock()

    def increment(self):
        with self.lock:
            self.time += random.randint(1, 5)
            print(f"Process {self.process_id} internal event. Time: {self.time}")

    def send_message(self, other):
        with self.lock:
            send_time = self.time
            print(f"Process {self.process_id} sends message to Process {other.process_id} at Time: {send_time}")
            other.receive_message(send_time)

    def receive_message(self, send_time):
        with self.lock:
            self.time = max(self.time, send_time) + 1
            print(f"Process {self.process_id} received message. Updated Time: {self.time}")


def process_thread(clock):
    while True:
        time.sleep(random.uniform(0.5, 1.5))
        event_type = random.choice(['internal', 'send'])
        if event_type == 'internal':
            clock.increment()
        else:
            target_process = random.choice([p for p in clocks if p.process_id != clock.process_id])
            clock.send_message(target_process)


if __name__ == "__main__":
    num_processes = 3
    clocks = [PhysicalClock(i) for i in range(num_processes)]
    threads = [threading.Thread(target=process_thread, args=(clock,)) for clock in clocks]

    for thread in threads:
        thread.start()

    for thread in threads:
        thread.join()