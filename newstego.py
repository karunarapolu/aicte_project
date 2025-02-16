import cv2

def load_image(image_path):
    img = cv2.imread(image_path)
    if img is None:
        raise FileNotFoundError("Image not found at the given path.")
    return img

def encode_message(img, msg):
    n, m, z = 0, 0, 0
    for char in msg:
        # Write the ASCII value of the character into the image pixel
        img[n, m, z] = ord(char)
        n += 1
        m += 1
        z = (z + 1) % 3
    return img

def decode_message(img, msg_length):
    message = ""
    n, m, z = 0, 0, 0
    for _ in range(msg_length):
        message += chr(img[n, m, z])
        n += 1
        m += 1
        z = (z + 1) % 3
    return message

def save_image(img, filename):
    cv2.imwrite(filename, img)
