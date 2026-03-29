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
    
    # Initialize SIFT detector (increased nfeatures to find denser clusters)
    sift = cv2.SIFT_create(nfeatures=5000)
    
    # Detect keypoints and compute descriptors
    keypoints, descriptors = sift.detectAndCompute(gray, None)
    
    if descriptors is None or len(descriptors) < 3:
        return _encode_image(image), 0
        
    # Initialize Brute Force Matcher with L2 distance (Euclidean)
    bf = cv2.BFMatcher(cv2.NORM_L2, crossCheck=False)
    
    # Match descriptors against themselves!
    matches = bf.knnMatch(descriptors, descriptors, k=3)
    
    # Calculate displacement vectors for all potential clones
    good_matches_info = []
    
    SPATIAL_THRESHOLD = 40   
    
    for m_n_o in matches:
        if len(m_n_o) < 3:
            continue
            
        m, n, o = m_n_o[0], m_n_o[1], m_n_o[2]
        
        # Stricter Lowe's ratio test
        if n.distance < 0.65 * o.distance:
            pt1 = keypoints[m.queryIdx].pt
            pt2 = keypoints[n.trainIdx].pt
            
            # Calculate physical spatial distance between matched points
            spatial_dist = np.sqrt((pt1[0] - pt2[0])**2 + (pt1[1] - pt2[1])**2)
            
            if spatial_dist > SPATIAL_THRESHOLD:
                # Store sorted index pairs to avoid reverse matches
                pair = tuple(sorted((m.queryIdx, n.trainIdx)))
                
                # Calculate displacement vector (dx, dy)
                # Ensure vector direction is consistent by always going from smaller X to larger X
                if pt1[0] > pt2[0]:
                    dx = pt1[0] - pt2[0]
                    dy = pt1[1] - pt2[1]
                else:
                    dx = pt2[0] - pt1[0]
                    dy = pt2[1] - pt1[1]
                
                good_matches_info.append((pair, (dx, dy)))
                
    # Keep only unique matches
    unique_pairs = {}
    for pair, vec in good_matches_info:
        if pair not in unique_pairs:
            unique_pairs[pair] = vec

    # DISPLACEMENT VECTOR CLUSTERING
    # Genuine copy-move forgeries shift multiple pixels by the exact same vector.
    # We find groups of similar vectors to eliminate randomly identical natural textures.
    VECTOR_TOLERANCE = 15.0 # pixels
    MIN_CLUSTER_SIZE = 4 
    
    final_valid_pairs = set()
    pairs_list = list(unique_pairs.keys())
    vecs_list = list(unique_pairs.values())
    
    for i in range(len(pairs_list)):
        if pairs_list[i] in final_valid_pairs:
            continue
            
        v1 = vecs_list[i]
        cluster = [pairs_list[i]]
        
        for j in range(len(pairs_list)):
            if i == j: continue
            
            v2 = vecs_list[j]
            v_dist = np.sqrt((v1[0] - v2[0])**2 + (v1[1] - v2[1])**2)
            
            # If the displacement vector is nearly identical, add it to the cluster
            if v_dist <= VECTOR_TOLERANCE:
                cluster.append(pairs_list[j])
                
        # If we found a dense cluster pointing in the same direction, it's a forgery!
        if len(cluster) >= MIN_CLUSTER_SIZE:
            for p in cluster:
                final_valid_pairs.add(p)

    unique_matches = list(final_valid_pairs)
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
