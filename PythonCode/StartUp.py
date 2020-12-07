# -*- coding: utf-8 -*-
"""
Created on Wed Oct 28 13:21:15 2020

"""
import ImageProcessing
from ModifySettings import getVehicles
from Drone import Drone
import numpy as np
from ForceControlAlgorithm import ForceControlAlgorithm

def __StartUp():
    mass = 5
    forceStrength = 500000000;
    print("Starting up");
    client = ImageProcessing.connectToUnreal()
    
    droneNames = getVehicles();
    numDrones = len(droneNames)
    print(numDrones)
    drones = []

    # y,x,z
    initialPositions = np.array([[0, -2, -2], [0, 2, -2], [4, -2, -2]])

    # initializing AirSim Simulator


    positions = {}
    controller = ForceControlAlgorithm(forceStrength)
    # intializing drones
    for i in range(len(droneNames)):
        drone = Drone(i, "UAV" + str(i + 1), mass, client, controller)
        drones.append(drone)
        positions[drone.name] = np.array([0, 0, 0])

    masterDroneName = drones[0].name
    while True:

        for i in range(0, len(drones)):
            gpsData = client.getGpsData(vehicle_name=drones[i].name);
            pos = np.array([gpsData.gnss.geo_point.latitude,gpsData.gnss.geo_point.longitude,gpsData.gnss.geo_point.altitude])
            positions[drones[i].name] = pos#client.getGpsData(vehicle_name=drones[i].name)#ImageProcessing.getLocalPosition(client, [], [masterDroneName, drones[i].name])
            drones[i].position = positions[drones[i].name]
            print(drones[i].name, drones[i].position)

        for i in range(1, len(drones)):
            force = np.zeros(3)
            for j in range(0, len(drones)):
                if i == j:
                    continue
                calcForce = drones[i].controlAlgorithm.computeMovementForce(drones[i], drones[j])
                print(calcForce)
                if j == 0:
                    force = force - calcForce
                else:
                    force = force + calcForce
            print(i, force)
            drones[i].moveDrone(force)

__StartUp()