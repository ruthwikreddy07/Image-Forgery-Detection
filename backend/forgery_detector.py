import cv2
import numpy as np
import base64

def detect_forgery(image_bytes):
    # Convert image bytes to numpy array
    nparr = np.frombuffer(image_bytes, np.uint8)
    # Decode the array to an OpenCV image
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    
    if image is None:
        raise ValueError("Invalid image format.")

    # Convert to grayscale for feature extraction
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    
    # Initialize SIFT detector (much more robust than ORB for copy-move detection)
    sift = cv2.SIFT_create(nfeatures=3000)
    
    # Detect keypoints and compute descriptors
    keypoints, descriptors = sift.detectAndCompute(gray, None)
    
    if descriptors is None or len(descriptors) < 3:
        return _encode_image(image), 0
        
    # Initialize Brute Force Matcher with L2 distance (Euclidean for SIFT)
    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=False)
    
    # Match descriptors against themselves!
    # k=3 because: 
    # match 1 is the point matching itself (dist = 0)
    # match 2 is the potential copy-moved point
    # match 3 is the closest unrelated point (for Lowe's ratio test)
    matches = bf.knnMatch(descriptors, descriptors, k=3)
    
    good_matches = []
    
    # Minimum pixel distance between point A and point B to avoid adjacent pixel matches
    SPATIAL_THRESHOLD = 40   
    
    for m_n_o in matches:
        if len(m_n_o) < 3:
            continue
            
        m, n, o = m_n_o[0], m_n_o[1], m_n_o[2]
        
        # Adapted Lowe's ratio test for self-similarity
        # We compare the 2nd best match (potential clone) to the 3rd best match (unrelated point)
        if n.distance < 0.75 * o.distance:
            # Get the coordinates of the matching keypoints
            pt1 = keypoints[m.queryIdx].pt
            pt2 = keypoints[n.trainIdx].pt
            
            # Calculate physical spatial distance between matched points
            spatial_dist = np.sqrt((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2)
            
            # Only consider points that are far apart (ignores immediate neighbors/noise)
            if spatial_dist > SPATIAL_THRESHOLD:
                # Store the index pairs to avoid duplicate reverse matches
                pair = tuple(sorted((m.queryIdx, n.trainIdx)))
                good_matches.append(pair)
                
    # Remove duplicates
    unique_matches = list(set(good_matches))
    
    number_of_forged_features = len(unique_matches)
    
    # Draw matches on the original image directly
    output_image = image.copy()
    
    # Draw thick colorful lines connecting identical duplicated regions
    for match in unique_matches:
        idx1, idx2 = match
        pt1 = tuple(map(int, keypoints[idx1].pt))
        pt2 = tuple(map(int, keypoints[idx2].pt))
        
        cv2.line(output_image, pt1, pt2, (0, 255, 255), 2)  # Yellow Cyan line
        cv2.circle(output_image, pt1, 4, (0, 0, 255), -1)   # Red dot
        cv2.circle(output_image, pt2, 4, (0, 0, 255), -1)   # Red dot
        
    encoded_str = _encode_image(output_image)
    return encoded_str, number_of_forged_features
    
def _encode_image(img):
    _, buffer = cv2.imencode('.jpg', img)
    base64_img = base64.b64encode(buffer).decode('utf-8')
    return base64_img
