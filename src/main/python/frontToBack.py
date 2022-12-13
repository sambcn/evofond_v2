from back.profile import Profile
from back.rectangularSection import RectangularSection
from back.trapezoidalSection import TrapezoidalSection
from utils import convertGranuloFromFrontToBack, SEDIMENT_TRANSPORT_LAW_DICT, AVAILABLE_HYDRAULIC_MODEL, AVAILABLE_LIMITS

import matplotlib.pyplot as plt
import numpy as np

def simulateModel(project, model, frontBuffer=None):
    """
    Launch back computations with front data
    """
    if project==None or model==None:
        return
    if not(model.getBoolState(project)):
        raise ValueError(f"Modèle incomplet, veuillez vérifier le modèle '{model.name}' dans l'onglet modèle")
    frontprofile = project.getProfile(model.profile)
    df = frontprofile.data
    for i in range(df.shape[1]-1, -1, -1):
        df = df[~(df[df.columns[i]].isnull())]
    df = df.sort_values(by=df.columns[0], ascending=False)
    x = df.iloc[:,0].values.tolist()
    if x==[]:
        raise ValueError(f"Profil vide ('{model.profile}'), veuillez vérifier que la colonne des abscisses n'est pas vide et que les lignes sont complètement remplies")
    maxi = max(x)
    x = [maxi - xi for xi in x]
    listOfSection = []
    if frontprofile.type == "Rectangular":
        for i in range(df.shape[0]):
            granuloName = frontprofile.getGranuloName(df.iloc[i][0])
            g = project.getGranulometry(granuloName)
            if g == None:
                raise ValueError(f"Pas de granulométrie renseignée pour x={df.iloc[i][0]} dans le profil '{model.profile}'")
            granulometry = convertGranuloFromFrontToBack(g)


            listOfSection.append(RectangularSection(x[i], df.iloc[i][1], df.iloc[i][3], df.iloc[i][2], granulometry=granulometry))
    elif frontprofile.type == "Trapezoidal":
        for i in range(df.shape[0]):
            granuloName = frontprofile.getGranuloName(df.iloc[i][0])
            granulometry = convertGranuloFromFrontToBack(project.getGranulometry(granuloName))
            listOfSection.append(TrapezoidalSection(x=x[i], z=df.iloc[i][1], z_min=df.iloc[i][2], b0=df.iloc[i][3], b0_min=df.iloc[i][4], f_left=df.iloc[i][5], f_right=df.iloc[i][6], granulometry=granulometry))
    profile = Profile(listOfSection)
    
    if model.interpolation:
        profile.complete(model.dx)

    df = project.getHydrogram(model.hydrogram).data
    for i in range(df.shape[1]-1, -1, -1):
        df = df[~(df[df.columns[i]].isnull())]
    t_hydro = df.iloc[:,0].values.tolist()
    Q = df.iloc[:,1].values.tolist()

    df = project.getSedimentogram(model.sedimentogram).data
    for i in range(df.shape[1]-1, -1, -1):
        df = df[~(df[df.columns[i]].isnull())]
    t_sedimento = df.iloc[:,0].values.tolist()
    Qs = df.iloc[:,1].values.tolist()
    if t_hydro[0] < t_sedimento[0] or t_hydro[-1] > t_sedimento[-1]:
        raise ValueError(f"Les instants de l'hydrogramme '{model.hydrogram}' ne sont pas inclus dans ceux du sédimentogramme '{model.sedimentogram}'. \n\n Veuillez modifier cela pour que l'algorithme puisse connaître le débit solide à chaque instant de l'évènement hydraulique.")
    Qs = np.interp(t_hydro, t_sedimento, Qs)
    law = SEDIMENT_TRANSPORT_LAW_DICT[model.sedimentTransportLaw]()
    
    if model.upstreamCondition == AVAILABLE_LIMITS[0]:
        upstreamCondition = model.upstreamCondition 
    elif model.upstreamCondition == AVAILABLE_LIMITS[1]:
        upstreamCondition = "critical_depth"
    elif model.upstreamCondition == AVAILABLE_LIMITS[2]:
        upstreamCondition = "normal_depth"

    if model.downstreamCondition == AVAILABLE_LIMITS[0]:
        downstreamCondition = model.downstreamCondition 
    elif model.downstreamCondition == AVAILABLE_LIMITS[1]:
        downstreamCondition = "critical_depth"
    elif model.downstreamCondition == AVAILABLE_LIMITS[2]:
        downstreamCondition = "normal_depth"

    # profile.compute_depth(Q[0], plot=True, friction_law=model.frictionLaw, upstream_condition=upstreamCondition, downstream_condition=downstreamCondition)
    # plt.show()
    # return None
    cfl = None if model.dt != None else model.cfl
    result = profile.compute_event(hydrogram=Q, t_hydrogram=t_hydro, law=law, sedimentogram=Qs, friction_law=model.frictionLaw, critical=(model.hydroModel==AVAILABLE_HYDRAULIC_MODEL[0]), upstream_condition=upstreamCondition, downstream_condition=downstreamCondition, plot=False, frontBuffer=frontBuffer, cfl=cfl, dt=model.dt, dt_save=model.dtForSave)
    
    return result