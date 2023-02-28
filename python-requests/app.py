import requests
import sys
import threading
import time

completed_requests = 0

def execute_requests(session, url):
    global completed_requests
    while True:
        with session.get(url) as response:
            response.text
        completed_requests += 1

def print_results(requests, duration):
    requests_per_second = requests / duration
    print(f'Completed {requests:,} requests in {duration:.2f} seconds ({requests_per_second:,.0f} req/s)')
    print()

def collect_results(title, duration):
    global completed_requests
    print(f'=== {title} ===')

    start = time.perf_counter()
    completed_requests = 0
    time.sleep(duration)
    end = time.perf_counter()

    print_results(completed_requests, end - start)

def main():
    if len(sys.argv) == 1:
        print('Usage: app <url> <parallel> <warmup> <duration>')
        return

    insecure = False
    if '--insecure' in sys.argv:
        insecure = True
        sys.argv.remove('--insecure')

    url = sys.argv[1]
    parallel = int(sys.argv[2]) if len(sys.argv) >= 3 else 64
    warmup = int(sys.argv[3]) if len(sys.argv) >= 4 else 10
    duration = int(sys.argv[4]) if len(sys.argv) >= 5 else 10

    print('=== Parameters ===')
    print(f'Url: {url}')
    print(f'Parallel: {parallel}')
    print(f'Warmup: {warmup}')
    print(f'Duration: {duration}')
    print(f'Insecure: {insecure}')
    print()

    with requests.Session() as session:
        if insecure:
            session.verify = False
            requests.packages.urllib3.disable_warnings(requests.packages.urllib3.exceptions.InsecureRequestWarning)

        threads = []
        for _ in range(parallel):
            thread = threading.Thread(target=lambda: execute_requests(session, url))
            thread.daemon = True
            threads.append(thread)
            thread.start()
        collect_results('Warmup', warmup)
        collect_results('Test', duration)

main()