import numpy as np

class Question3_Solver:
    def __init__(self):
        return;

    # Add your code here.
    # Return the centroids of clusters.
    # You must use [(30, 30), (150, 30), (90, 130)] as initial centroids
    def solve(self, points):
        centroids = [(30, 30), (150, 30), (90, 130)];
        
        while(True):
            new_centroid = self.computecentroid(points,len(centroids), centroids)                             
            if centroids == new_centroid:
                break
            centroids = new_centroid           
        return centroids;
    
    def get_distance(self,x,y):
        return np.sqrt((x[0]-y[0])**2+ (x[1]-y[1])**2)
    
    def get_cluster_index(self, point, centroids):
        distances = list()
        for centroid in centroids:
            distances.append(self.get_distance(point,centroid))
        return np.argmin(distances)
        
    def computecentroid(self,points,k,centroids):
        clusters = list()
        for i in range(0,k):
            clusters.append(list()) 
            
        for point in points:
            cluster_index = self.get_cluster_index(point,centroids)
            clusters[cluster_index].append(point)
        
        centroids = list()
        for cluster in clusters:
            sum_x = 0
            sum_y = 0
            for point in cluster:
                sum_x += point[0]
                sum_y += point[1] 
            centroids.append((int(sum_x)/len(cluster),int(sum_y)/len(cluster)))
        
        return centroids
