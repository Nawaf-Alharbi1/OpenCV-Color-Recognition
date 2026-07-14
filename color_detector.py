import cv2
import urllib.request
import json

backup_database = {
    "Red": (255, 0, 0), "Green": (0, 255, 0), "Blue": (0, 0, 255),
    "Yellow": (255, 255, 0), "Orange": (255, 165, 0), "Purple": (128, 0, 128),
    "Pink": (255, 192, 203), "Brown": (165, 42, 42), "Cyan": (0, 255, 255)
}

colors_database = {}

def hex_to_rgb(hex_str):
    hex_str = hex_str.lstrip('#')
    return tuple(int(hex_str[i:i+2], 16) for i in (0, 2, 4))

print("Loading color database...")
xkcd_url = "https://raw.githubusercontent.com/dariusk/corpora/master/data/colors/xkcd.json"

try:
    with urllib.request.urlopen(xkcd_url, timeout=5) as response:
        data = json.loads(response.read().decode())
        for item in data['colors']:
            color_name = item['color'].title()
            rgb_val = hex_to_rgb(item['hex'])
            colors_database[color_name] = rgb_val
    print(f"{len(colors_database)} colors loaded successfully.")
except Exception as e:
    print("Internet unavailable. Using backup color database.")
    colors_database = backup_database

def get_closest_color(r, g, b):
    rgb_max = max(r, g, b)
    rgb_min = min(r, g, b)
    
    if (rgb_max - rgb_min) < 22:
        average_value = (r + g + b) / 3
        if average_value > 215:
            return "White"
        elif average_value < 45:
            return "Black"
        else:
            return "Gray"
            
    minimum_distance = float('inf')
    closest_color_name = "Unknown"
    
    for color_name, rgb_value in colors_database.items():
        distance = (r - rgb_value[0])**2 + (g - rgb_value[1])**2 + (b - rgb_value[2])**2
        if distance < minimum_distance:
            minimum_distance = distance
            closest_color_name = color_name
            
    return closest_color_name

def click_event(event, x, y, flags, param):
    if event == cv2.EVENT_LBUTTONDOWN:
        bgr_pixel = img[y, x]
        b, g, r = int(bgr_pixel[0]), int(bgr_pixel[1]), int(bgr_pixel[2])
        
        color_name = get_closest_color(r, g, b)
        display_text = f"RGB:({r},{g},{b}) - {color_name}"
        
        print(f"Click at ({x}, {y}) | Detected color: {color_name} | RGB: ({r}, {g}, {b})")
        
        img_height, img_width = img.shape[:2]
        (text_width, text_height), _ = cv2.getTextSize(display_text, cv2.FONT_HERSHEY_SIMPLEX, 0.42, 1)
        
        text_x = x + 12
        text_y = y + 5
        
        if text_x + text_width > img_width:
            text_x = x - 12 - text_width
        if text_y - text_height < 5:
            text_y = y + 15
        if text_y > img_height - 5:
            text_y = y - 10

        cv2.circle(img_display, (x, y), 5, (0, 0, 0), -1)
        cv2.circle(img_display, (x, y), 3, (255, 255, 255), -1)
        
        cv2.putText(img_display, display_text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (0, 0, 0), 3, cv2.LINE_AA)
        cv2.putText(img_display, display_text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.42, (255, 255, 255), 1, cv2.LINE_AA)
        
        cv2.imshow('Super Color Detector 950+', img_display)

image_path = 'RGB test.jpg'  
img = cv2.imread(image_path)

if img is None:
    print("Error: Image not found! Please check the filename and path.")
    exit()

img_display = img.copy()

cv2.namedWindow('Super Color Detector 950+')
cv2.setMouseCallback('Super Color Detector 950+', click_event)

cv2.imshow('Super Color Detector 950+', img_display)
cv2.waitKey(0)
cv2.destroyAllWindows()