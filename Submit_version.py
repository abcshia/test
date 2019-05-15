import numpy as np
import pandas as pd
import os,inspect
import pickle
import googlemaps
import gmplot
# Get this current script file's directory:
loc = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
# Set working directory
os.chdir(loc)
# to avoid tk crash
import matplotlib
matplotlib.use('Qt5Agg')
import matplotlib.pyplot as plt
import matplotlib.colors as colors

## Toy example

# Load google api key
with open('api-key.txt','r') as f:
    apikey = f.read()

# address list
address_list = ['22 Peace Plaza Suite 400, San Francisco, CA 94115',
                '32115 Union Landing Blvd, Union City, CA 94587',
                '4370 Thornton Ave, Fremont, CA 94536',
                '668 Barber Ln, Milpitas, CA 95035',
                '447 Great Mall Dr, Milpitas, CA 95035',
                '655 Knight Way, Stanford, CA 94305',
                '2855 Stevens Creek Blvd, Santa Clara, CA 95050'
                ]
                
# Set origins and destinations
origins = address_list
destinations = address_list


# Distance matrix querry:
gmaps = googlemaps.Client(key=apikey)
dmatrix = gmaps.distance_matrix(origins, destinations, mode='driving') # departure_time, arrival_time

# # Load
# with open('dmatrix.pickle','rb') as f:
#     dmatrix = pickle.load(f)

# get the distances and durations
rows = dmatrix['rows']
o_id = 0 # origin id
d_id = 0 # destination id

dist_list = []
dura_list = []
for o_id,origin in enumerate(origins):
    od_dist = []
    od_dura = []
    for d_id,destination in enumerate(destinations):
        distance = rows[o_id]['elements'][d_id]['distance']['value'] # [m]
        duration = rows[o_id]['elements'][d_id]['duration']['value'] # [sec]
        od_dist.append(distance)
        od_dura.append(duration)
    dist_list.append(od_dist)
    dura_list.append(od_dura)
        
# Physical driving distance data frame
df_dist = pd.DataFrame(dist_list,columns=['Dest{}'.format(d) for d in range(len(destinations))],index=['Orig{}'.format(o) for o in range(len(origins))])

# Travel time distance data frame
df_dura = pd.DataFrame(dura_list,columns=['Dest{}'.format(d) for d in range(len(destinations))],index=['Orig{}'.format(o) for o in range(len(origins))])
        

## MDS
from sklearn.manifold import MDS
mds = MDS(n_components=2, max_iter=3000,dissimilarity="precomputed")

dist_mat = df_dist.values
dura_mat = df_dura.values
# make symmetric by averaging
dist_mat = (dist_mat + dist_mat.T)/2
dura_mat = (dura_mat + dura_mat.T)/2

X_dist = mds.fit(dist_mat)
dist = X_dist.embedding_

plt.figure(0)
plt.scatter(dist[:,0],dist[:,1])
for i,xy in enumerate(dist):
    plt.text(xy[0],xy[1],'{}'.format(i),fontsize=12)
plt.show()


X_dura = mds.fit(dura_mat)
dura = X_dura.embedding_

plt.figure(1)
plt.scatter(dura[:,0],dura[:,1])
for i,xy in enumerate(dura):
    plt.text(xy[0],xy[1],'{}'.format(i),fontsize=12)
plt.show()


# Scale the plots to compare
from sklearn.preprocessing import normalize
dist_norm = normalize(dist,axis=0)
dura_norm = normalize(dura,axis=0)

plt.figure(0)
plt.scatter(dist_norm[:,0],dist_norm[:,1])
for i,xy in enumerate(dist_norm):
    plt.text(xy[0],xy[1],'{}'.format(i),fontsize=12)
plt.show()

plt.figure(1)
plt.scatter(dura_norm[:,0],dura_norm[:,1])
for i,xy in enumerate(dura_norm):
    plt.text(xy[0],xy[1],'{}'.format(i),fontsize=12)
plt.show()

# combined plot
plt.figure(2)
plt.scatter(dura_norm[:,0],dura_norm[:,1],color='blue',label='MDS retrieved duration')
for i,xy in enumerate(dura_norm):
    plt.text(xy[0],xy[1],'{}'.format(i),fontsize=12)
    
plt.scatter(dist_norm[:,0],dist_norm[:,1],color='red',label='MDS retrieved distance')
for i,xy in enumerate(dist_norm):
    plt.text(xy[0],xy[1],'{}'.format(i),fontsize=12)
plt.legend()
plt.xlabel('a.u.')
plt.ylabel('a.u.')
plt.title('Scaled travel time/distance for comparison')
plt.show()


## Mark on Google Maps

# Geocoding:

geocodes = []
latlngs_address = []
for i,address in enumerate(address_list):
    geocode = gmaps.geocode(address_list[i])
    geocodes.append(geocode[0])
    
    lat,lng = geocode[0]['geometry']['location']['lat'],geocode[0]['geometry']['location']['lng']
    latlngs_address.append([lat,lng,address])


latlng_arr = np.array(latlngs_address)
latlng_arr = np.array(latlng_arr[:,:2],dtype=np.float)


## Plot

# plot distances/durations
n_dist_mat = dist_mat/dist_mat.max()
n_dura_mat = dura_mat/dura_mat.max()

gmap = gmplot.GoogleMapPlotter(37.6221449,-122.3041143,10.21)
gmap.scatter(latlng_arr[:,0],latlng_arr[:,1],'red',size=20)

# Mark locations
for xy in latlng_arr: # markers cannot take vectors, mark them one by one
    gmap.marker(xy[0],xy[1],'#FF5555')

# Set up color code
color1 = np.array([0, 0, 1,0.5])
color2 = np.array([1, 0, 0,0.5])

def get_color(color1,color2,fraction=0.5):
    color = (color2-color1)*fraction + color1
    color = colors.rgb2hex(color)
    return(color)


N = latlng_arr.shape[0]
for o in range(N):
    for d in range(N):
        xs = [latlng_arr[o,0], latlng_arr[d,0]]
        ys = [latlng_arr[o,1], latlng_arr[d,1]]

        color_dist = get_color(color1,color2,n_dist_mat[o,d])
        gmap.plot(xs,ys,color_dist)
        
        color_dura = get_color(color1,color2,n_dura_mat[o,d])
        gmap.plot(xs,ys,color_dura)
        
gmap.apikey = apikey
gmap.draw("my_geocode.html")


    
    
    
    
    
    
    
    
    
  





