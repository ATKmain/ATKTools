import tensorflow as tf
import time
import numpy as np

def benchmark_tensorflow_gpu():
    # Check if TensorFlow can access GPU
    gpus = tf.config.list_physical_devices('GPU')
    if not gpus:
        print("GPU not found. Using CPU instead.")
    else:
        for gpu in gpus:
            print("Found GPU: ", gpu)

    # Parameters for the matrix sizes
    size = 10000  # Size of the square matrix
    repeats = 1000  # How many times to repeat the operation

    # Generate two random matrices
    a = tf.random.normal([size, size], dtype=tf.float32)
    b = tf.random.normal([size, size], dtype=tf.float32)

    # Warm-up run, not measured
    tf.matmul(a, b)

    # Benchmark
    start_time = time.time()
    for _ in range(repeats):
        if _ % 100 == 0:
            print(f"Step {_}")
        tf.matmul(a, b)
    end_time = time.time()

    # Calculate and print average time
    avg_time = (end_time - start_time) / repeats
    print(f"Average time per multiplication: {avg_time:.5f} seconds")

if __name__ == "__main__":
    benchmark_tensorflow_gpu()
