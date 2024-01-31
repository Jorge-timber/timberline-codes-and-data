##Code to extract altitude variation and distance between multiple pairs of points
# Load vector layer for the 'before' data
antes = QgsVectorLayer(r"C:\points_before.shp")

# Load vector layer for the 'after' data
despues = QgsVectorLayer(r"C:\points_after.shp")

# Initialize an empty list for altitudes before the event
puntos_antes_alts = []

# Extract features from the 'before' dataset
features1 = antes.getFeatures()
for feature in features1:
    p1 = feature.attribute('mdt02_buen')
    puntos_antes_alts.append(p1)
    
# Initialize an empty list for altitudes after the event
puntos_despues_alts = []

# Extract features from the 'after' dataset
features2 = despues.getFeatures()
for feature in features2:
    p2 = feature.attribute('mdt02_buen')
    puntos_despues_alts.append(p2)
    
# Create a QgsDistanceArea object without defining the ellipsoid
# dis = QgsDistanceArea()

# Calculate altitude differences
alturas = []
for a, b in zip(puntos_antes_alts, puntos_despues_alts):
    d = round(b - a, 2)
    alturas.append(d)
    
# Load the vector layer for the points after the event
capa_puntos = QgsVectorLayer(r"C:\points_after_alt.shp")

# Define the name and type of the new field
nombre_campo = 'var_alt'
tipo_campo = QVariant.Double

# Check if the new field exists and create it if not
if nombre_campo not in capa_puntos.fields().names():
    campo_nuevo = QgsField(nombre_campo, tipo_campo, 'double', 4, 2)
    capa_puntos.startEditing()
    capa_puntos.addAttribute(campo_nuevo)
    capa_puntos.updateFields()
    capa_puntos.commitChanges()

# Check if the field exists in the layer and update it
if nombre_campo in capa_puntos.fields().names():
    indice_campo = capa_puntos.fields().names().index(nombre_campo)
    capa_puntos.startEditing()
    for feature in capa_puntos.getFeatures():
        altura = alturas[feature.id()]
        feature[indice_campo] = altura
        capa_puntos.updateFeature(feature)
    capa_puntos.commitChanges()

# Extract point geometries before the event
puntos_antes = []
features1 = antes.getFeatures()
for feature in features1:
    p1 = feature.geometry().asPoint()
    puntos_antes.append(p1)
    
# Extract point geometries after the event
puntos_despues = []
features2 = despues.getFeatures()
for feature in features2:
    p2 = feature.geometry().asPoint()
    puntos_despues.append(p2)
    
# Create a QgsDistanceArea object and define the ellipsoid
dis = QgsDistanceArea()
dis.setEllipsoid('GRS80')

# Calculate distances
distancias = []
for a, b in zip(puntos_antes, puntos_despues):
    e = round(a.distance(b), 2)
    distancias.append(e)

# Define the name and type of the new field for distance
nombre_campo2 = 'distancia'
tipo_campo2 = QVariant.Double

# Check if the new field for distance exists and create it if not
if nombre_campo2 not in capa_puntos.fields().names():
    campo_nuevo2 = QgsField(nombre_campo2, tipo_campo2, 'double', 4, 2)
    capa_puntos.startEditing()
    capa_puntos.addAttribute(campo_nuevo2)
    capa_puntos.updateFields()
    capa_puntos.commitChanges()

# Check if the distance field exists in the layer and update it
if nombre_campo2 in capa_puntos.fields().names():
    indice_campo2 = capa_puntos.fields().names().index(nombre_campo2)
    capa_puntos.startEditing()
    for feature in capa_puntos.getFeatures():
        distancia = distancias[feature.id()]
        feature[indice_campo2] = distancia
        capa_puntos.updateFeature(feature)
    capa_puntos.commitChanges()