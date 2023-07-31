import React, { useState, useEffect } from 'react';
import AttributeTracker from './attributeTracker';
import CitiesContainer from './citiesContainer';
import TestingCities from './testingCities';
function Information({activitiesInfo, tripFull, citiesInfo, showLeftColumn, setShowLeftColumn}) {

    const togglePosition = () => {
        setShowLeftColumn((current) => !current)
    }

    if (showLeftColumn){
        return <>
        <CitiesContainer
        citiesInfo={citiesInfo}
        tripFull={tripFull}
        />

        <div class="d-grid gap-2"> <button class="btn btn-primary" type="button" onClick={togglePosition}>Toggle Cities View</button> </div>
        </>

    }
    else {
    return <>
        <AttributeTracker
            attributeName={activitiesInfo.activities.name}
            attributeLimit={activitiesInfo.activities.limit}
            attributeList={activitiesInfo.activities.list}
        />
        <AttributeTracker
            attributeName={activitiesInfo.climate.name}
            attributeLimit={activitiesInfo.climate.limit}
            attributeList={activitiesInfo.climate.list}
        />
        <AttributeTracker
            attributeName={activitiesInfo.location.name}
            attributeLimit={activitiesInfo.location.limit}
            attributeList={activitiesInfo.location.list}
        />
        <AttributeTracker
            attributeName={activitiesInfo.travelMethod.name}
            attributeLimit={activitiesInfo.travelMethod.limit}
            attributeList={activitiesInfo.travelMethod.list}
        />
        <AttributeTracker
            attributeName={activitiesInfo.tripDuration.name}
            attributeLimit={activitiesInfo.tripDuration.limit}
            attributeList={activitiesInfo.tripDuration.list}
        />
        <AttributeTracker
            attributeName={activitiesInfo.budget.name}
            attributeLimit={activitiesInfo.budget.limit}
            attributeList={activitiesInfo.budget.list}
        />
        {tripFull && <div class="d-grid gap-2"> <button class="btn btn-primary" type="button" onClick={togglePosition}>Toggle Cities View</button> </div>}
    </>  
   
    }
    
}
export default Information