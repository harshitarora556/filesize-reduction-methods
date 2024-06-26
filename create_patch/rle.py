import os
import time
import psutil


def run_length_encode(data):
    """Encodes input data using run-length encoding.
    :returns encoded: bytearray() """

    encoded = bytearray()
    cnt = 1
    prev = data[0]

    for c_byte in data:
        if c_byte != prev:
            if cnt > 0:
                encoded.extend(cnt.to_bytes(2, 'big'))
            encoded.append(prev)
            prev = c_byte
            cnt = 1
        else:
            cnt += 1

    if cnt > 0:
        encoded.extend(cnt.to_bytes(2, byteorder='big'))
        encoded.append(prev)

    return encoded


def run_length_decode(encoded_data):
    """Decodes a run-length encoded byte array.
    :returns decoded: bytearray() """

    decoded = bytearray()
    i = 0
    lim = len(encoded_data)
    while i < lim:
        cnt = int.from_bytes(encoded_data[i: i+2], byteorder='big')
        i += 2
        for x in range(cnt):
            decoded.append(encoded_data[i])
        i += 1
    return decoded


def calculate_size_reduction(original_size, data_size):
    """Calculates the percentage reduction in file size after encoding.
    :returns reduction: float"""

    if original_size == 0:
        return float('inf')  # Handle division by zero
    reduction = ((original_size - data_size) / original_size) * 100
    return reduction


# Function to monitor CPU utilization and memory usage
def monitor_resource_usage():
    cpu_percent = psutil.cpu_percent()
    memory_usage = psutil.virtual_memory().percent
    return cpu_percent, memory_usage


def main():
    files = ["xor.bin", "GAP5-1RF_Rev07_IV02_old.bin", "GAP5-1RF_Rev08_IV00_new.bin"]
    for file in files:
        print(f"\n\n For file {file} : \n")

        with open(file, "rb") as infile:
            data = infile.read()

        # Track CPU and memory usage before compression
        cpu_before, memory_before = monitor_resource_usage()
        start = time.time()
        encoded_data = run_length_encode(data)
        end = time.time()
        encoding_time = end - start

        # Track CPU and memory usage during compression
        cpu_during_compression, memory_during_compression = monitor_resource_usage()
        with open(f"encoded_{file}", "wb") as outfile:
            outfile.write(encoded_data)

        # Track CPU and memory usage before decompression
        cpu_before_decompression, memory_before_decompression = monitor_resource_usage()
        start = time.time()
        decoded_data = run_length_decode(encoded_data)
        end = time.time()
        decoding_time = end - start

        # Track CPU and memory usage during decompression
        cpu_during_decompression, memory_during_decompression = monitor_resource_usage()
        with open(f"decoded_{file}", "wb") as outfile:
            outfile.write(decoded_data)

        original_size = os.stat(file).st_size  # bytes
        encoded_size = os.stat(f"encoded_{file}").st_size  # bytes
        decoded_size = os.stat(f"decoded_{file}").st_size  # bytes

        reduction1 = calculate_size_reduction(original_size, encoded_size)
        reduction2 = calculate_size_reduction(original_size, decoded_size)
        loss = reduction2
        reproducibility = 100 - loss
        print(f"Size reduction achieved by encoding: {reduction1:.2f}%")
        print(f"Size reduction from original after decoding: {reduction2:.2f}%")
        print(f"Hence Reproducibility = {reproducibility:.2f}%")
        print(f"Loss = {loss:.2f}%")
        print("Encoding time: ", encoding_time, " s.")
        print("Decoding time: ", decoding_time, " s.")
        print("CPU utilization during compression:", cpu_during_compression - cpu_before, "%")
        print("Memory usage during compression:", memory_during_compression - memory_before, "%")
        print("CPU utilization during decompression:", cpu_during_decompression - cpu_before_decompression, "%")
        print("Memory usage during decompression:", memory_during_decompression - memory_before_decompression, "%")

    print("Results:")
    print("Positive Compression: Reduction in size")
    print("Negative compression: Increment in size")
    print("RLE works best when there are long runs of repeating data")


if __name__ == "__main__":
    main()