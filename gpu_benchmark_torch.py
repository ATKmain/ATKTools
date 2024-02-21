import torch
import time

def benchmark_gpu():
    # Size of the matrices to multiply
    size = 10000
    # Number of times to repeat the operation for averaging
    repeats = 1200

    # Ensures that CUDA is available and selects the default GPU
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    print(f"Using device: {device}")

    # Initialize two random matrices
    a = torch.rand(size, size, device=device)
    b = torch.rand(size, size, device=device)

    # Warm-up run, not measured
    torch.matmul(a, b)

    # Benchmark
    start_time = time.time()
    for _ in range(repeats):
        if _ % 100 == 0:
            print(f"Step {_}")
        torch.matmul(a, b)
    end_time = time.time()

    # Calculate and print average time
    avg_time = (end_time - start_time) / repeats
    print(f"Average time per multiplication: {avg_time:.5f} seconds")

if __name__ == "__main__":
    print("GPU benchmark using PyTorch")
    print(f"PyTorch version: {torch.__version__}")
    print("Device count: " + str(torch.cuda.device_count()))
    print("GPU Device name" + torch.cuda.get_device_name(0))

    if torch.cuda.is_available():
        try:
            print("GPU Device name: " + torch.cuda.get_device_name(0))
        except RuntimeError as e:
            print("Error accessing GPU properties: ", e)
    else:
        print("CUDA is not available.")

    benchmark_gpu()
