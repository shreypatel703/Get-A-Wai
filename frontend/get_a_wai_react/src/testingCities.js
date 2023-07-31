import React from 'react';
import CityObject from './cityObject';

function TestingCities() {

    const citiesInfo = 
        {
            citiesList: [
                {name: "City Name 1",
                cityID: 1,
                imgLink: "logo192.png",
                travelMethod: "car",
                travelTimeEstimate: 21,
                estimatedCost: 1200,
                cityActivitiesList: ["Fishing", "Hiking", "Clubbing", "Gambling", "Beaches"]},
                {name: "City Name 2",
                cityID: "2",
                imgLink: "logo192.png",
                travelMethod: "plane",
                travelTimeEstimate: 11,
                estimatedCost: 900,
                cityActivitiesList: ["City_acts","Fishing", "Hiking", "Clubbing", "Gambling", "Beaches"]},
                {name: "City Name 3",
                cityID: "2",
                imgLink: "logo192.png",
                travelMethod: "plane",
                travelTimeEstimate: 11,
                estimatedCost: 900,
                cityActivitiesList: ["City_acts","Fishing", "Hiking", "Clubbing", "Gambling", "Beaches"]},
                {name: "City Name 4",
                cityID: "2",
                imgLink: "logo192.png",
                travelMethod: "plane",
                travelTimeEstimate: 11,
                estimatedCost: 900,
                cityActivitiesList: ["City_acts","Fishing", "Hiking", "Clubbing", "Gambling", "Beaches"]},
                {name: "City Name 5",
                cityID: "2",
                imgLink: "logo192.png",
                travelMethod: "plane",
                travelTimeEstimate: 11,
                estimatedCost: 900,
                cityActivitiesList: ["City_acts","Fishing", "Hiking", "Clubbing", "Gambling", "Beaches"]},
                {name: "City Name 2",
                cityID: "2",
                imgLink: "logo192.png",
                travelMethod: "plane",
                travelTimeEstimate: 11,
                estimatedCost: 900,
                cityActivitiesList: ["City_acts","Fishing", "Hiking", "Clubbing", "Gambling", "Beaches"]}
            ],
            userBudget: 1000,
            userActivites: ["userAc1", "userAct2", ], 
            nights: 6
        }   



    return <>
        {citiesInfo.citiesList.map((city, index) => {
        return <div class="col"><CityObject
            key={index}
            rank={index + 1}
            cityName={city.name}
            cityID={city.cityID}
            imgLink={city.imgLink}
            travelMethod={city.travelMethod}
            travelTimeEstimate={city.travelTimeEstimate}
            estimatedCost={city.estimatedCost}
            cityActivitiesList={city.cityActivitiesList}
            userBudget={citiesInfo.userBudget}
            userActivities={citiesInfo.userActivities}
            nights={citiesInfo.nights}
        /></div>
    })}</>
    
}
export default TestingCities