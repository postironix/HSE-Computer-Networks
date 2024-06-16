import argparse
import icmplib
import sys

def find_min_mtu_in_path(dest, min, max):
    left, right = min, max
    while left <= right:
        mid = (left + right) // 2
        data_size = mid - 28
        try:
            ping_res = icmplib.ping(
                dest,
                payload_size=data_size,
            )
        except:
            print('Unknown ping error', flush=True)
            return 0

        print(f"Current MTU size {mid}", flush=True)
        if ping_res.is_alive:
            left = mid + 1
        else:
            right = mid - 1
    return right

def check_adress(dest):
    print(f"Checking if address {dest} is reachable", flush=True)
    result = icmplib.ping(dest)
    return result.is_alive

if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Path MTU discovery script')
    parser.add_argument('--address', type=str, required=True, help='Destination address')
    args = parser.parse_args()

    if not check_adress(args.address):
        print("Address is not reachable", flush=True)
        sys.exit(1)
    else:
        print("Address is reachable")

    min = 68
    max = 10000

    try:
        mtu = find_min_mtu_in_path(args.address, min, max)
        if mtu:
            print(f"The minimum MTU in path is: {mtu}", flush=True)
        else:
            print("Could not determine the MTU within the specified range.", flush=True)
    except Exception as e:
        print(f"An error occurred: {e}", flush=True)
        sys.exit(1)
