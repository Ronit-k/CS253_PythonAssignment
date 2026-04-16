import numpy as np

def sum_prod(region, kernel):
    total = 0
    for i in range(region.shape[0]):
        for j in range(region.shape[1]):
            total += region[i, j] * kernel[i, j]
    
    return max(0, min(255, int(total)))

def apply_filter(image, kernel):
    """
    Performs 2D convolution on an image using a given kernel.
    
    Args:
        image (numpy.ndarray): The input image as a 2D array.
        kernel (numpy.ndarray): The convolution kernel as a 2D array. given that it will be 3x3
        
    Returns:
        numpy.ndarray: The resulting image as a 2D array of type uint8.
    """
    img_h, img_w = image.shape
    ker_h, ker_w = kernel.shape # given that it will be 3x3, but generalizing to any size
    
    # Padding size, for 3x3 kernel, padding will be 1
    pad_h = ker_h // 2 
    pad_w = ker_w // 2 
    
    # Create padded image with zeros
    padded_image = np.zeros((img_h + 2 * pad_h, img_w + 2 * pad_w)) # create a matrix of zeros with size same as image + padding
    padded_image[ pad_h:(pad_h + img_h) , pad_w:(pad_w + img_w)] = image # copy the image to the center of the padded image
    
    # Output image, initialize with zeros
    output = np.zeros((img_h, img_w), dtype=np.uint8)
    
    for i in range(img_h):
        for j in range(img_w):
            # Extract the region of interest
            region = padded_image[i:i + ker_h, j:j + ker_w]
            # Element-wise multiplication and summation
            output[i, j] = sum_prod(region, kernel)
    
    return output

if __name__ == "__main__":
    img = np.array([
        [10, 10, 10],
        [10, 50, 10],
        [10, 10, 10]
    ])
    
    kernel = np.array([
        [-1, -1, -1],
        [-1,  8, -1],
        [-1, -1, -1]
    ])
    
    print(apply_filter(img, kernel))
