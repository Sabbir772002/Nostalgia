import numpy as np
from PIL import Image
import json

class ImageVectorService:
    @staticmethod
    def extract_vector(image_file_or_path):
        """
        Extracts a normalized 288-dimensional feature vector from an image.
        Combines:
        1. Spatial grid of average colors (8x8 grid * 3 channels = 192 features)
        2. Color histograms (32 bins * 3 channels = 96 features)
        The vector is L2 normalized so that cosine similarity = dot product.
        """
        try:
                                                                                 
            if isinstance(image_file_or_path, str):
                img = Image.open(image_file_or_path)
            else:
                                                      
                if hasattr(image_file_or_path, 'seek'):
                    image_file_or_path.seek(0)
                img = Image.open(image_file_or_path)

            img = img.convert('RGB')
            
                                                                                        
            img_grid = img.resize((8, 8), Image.Resampling.BILINEAR)
            grid_data = np.array(img_grid).astype(float) / 255.0
            spatial_vector = grid_data.flatten()
            
                                                                    
            np_img = np.array(img)
            hist_r, _ = np.histogram(np_img[:, :, 0], bins=32, range=(0, 256), density=True)
            hist_g, _ = np.histogram(np_img[:, :, 1], bins=32, range=(0, 256), density=True)
            hist_b, _ = np.histogram(np_img[:, :, 2], bins=32, range=(0, 256), density=True)
            hist_vector = np.concatenate([hist_r, hist_g, hist_b])
            
                                                           
            feature_vector = np.concatenate([spatial_vector, hist_vector])
            
                                                                      
            norm = np.linalg.norm(feature_vector)
            if norm > 0:
                feature_vector = feature_vector / norm
                
            return feature_vector.tolist()
        except Exception as e:
            print(f"Error extracting image vector: {e}")
            return None

    @staticmethod
    def calculate_similarity(vector1, vector2):
        """
        Calculates cosine similarity between two vectors.
        Since they are L2 normalized, similarity is simply the dot product.
        """
        if not vector1 or not vector2:
            return 0.0
        try:
            v1 = np.array(vector1)
            v2 = np.array(vector2)
            return float(np.dot(v1, v2))
        except Exception as e:
            print(f"Error calculating similarity: {e}")
            return 0.0
