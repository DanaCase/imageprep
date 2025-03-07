import cv2
import numpy as np
import matplotlib.pyplot as plt
import argparse

if __name__ == "__main__":
    argparse = argparse.ArgumentParser(description="Compare two images")
    argparse.add_argument("--actual", type=str, required=True)
    argparse.add_argument("--desired", type=str, required=True)
    args = argparse.parse_args()

    actual = cv2.imread(args.actual)
    desired = cv2.imread(args.desired)

# Compute absolute difference
    diff = cv2.absdiff(actual, desired)

# Convert to grayscale to highlight differences
    gray_diff = cv2.cvtColor(diff, cv2.COLOR_BGR2GRAY)

# Show the difference
    plt.imshow(gray_diff, cmap="hot")
    plt.colorbar()
    plt.title("Difference Between Generated and Reference Image")
    plt.savefig("diff.png")
    plt.close()
