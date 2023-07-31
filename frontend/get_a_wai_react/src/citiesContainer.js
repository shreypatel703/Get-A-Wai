import React from 'react';
import CityObject from './cityObject';
function CitiesContainer({citiesInfo, tripFull}) {
    console.log(citiesInfo)
    if (tripFull && citiesInfo !== undefined){
        return <>
        {citiesInfo.citiesList.map((city, index) => {
            return <div class="col"><CityObject 
                key={index}
                rank={index + 1}
                cityName={city.name}
                cityID={city.id}
                imgLink={`${city.id}.jpg`}
                travelMethod={city.travel_method}
                // travelTimeEstimate={city.travelTimeEstimate}
                estimatedCost={city.estimated_cost}
                cityActivitiesList={city.cityActivityList}
                userBudget={citiesInfo.userBudget}
                userActivities={citiesInfo.userActivities}
                nights={citiesInfo.nights}
            /></div>
        })}
        </>
    }
    else {
        return <>
        
        </>
    }
    
}
export default CitiesContainer