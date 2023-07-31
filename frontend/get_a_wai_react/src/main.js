import React, { useState, useEffect } from 'react';
import Information from './information';
import Chat from './chat';
import CitiesContainer from './citiesContainer';
import TestingCities from './testingCities';
import { v4 as uuid } from 'uuid';

const userId = uuid()

function Main() {
    
    const [attributeInfo_List, setAttributeInfo_List] = useState({
        "activities": {
            "name":"Activities",
            "limit": 3,
            "list": []  
        },
        "climate": {
            "name": "Climate",
            "limit": 1,
            "list": []
        },
        "location": {
            "name": "Location",
            "limit": 2,
            "list": []
        },
        "travelMethod": {
            "name": "Travel Method",
            "limit": 1,
            "list": []
        },
        "tripDuration": {
            "name": "Trip Length",
            "limit": 1,
            "list": []
        },
        "budget": {
            "name": "Budget",
            "limit": 1,
            "list": []
        }
    })

    // tracks if all datapoints are filled
    const [tripInfoIsFull, setTripInfoIsFull] = useState(false)

    // holds the recommened cities
    // examples
    // citiesObject = {
        //     citiesList: [
        //         {name: "<city_name>",
        //         cityID: "<citiesID>"
        //         imgLink: "<img_path>",
        //         travelMethod: "<travel_method>",
        //         travelTimeEstimate: "<time>",
        //         estimatedCost: "<calcualted_cost>",
        //         cityActivitiesList: [list_of_city_acticities]}, ..., {"more_of_the_above"} ]
        //     userBudget: "<given_user_budget>",
        //     userActivites: ["<userAc1>", "<userAct2>", ...] 
        //     nights: "<nights_spent>",
        // }
        

    const [citiesObject, setCitiesList] = useState()
    const [showCitiesLeftColumn, setShowCitiesLeftColumn] = useState(false)

    //checks if the all the attributes are full
    useEffect(()=>{
        let totalAttributeCount = 0
        let filledAttributeCount = 0
        for (const property in attributeInfo_List){
            if (attributeInfo_List[property].list.length === attributeInfo_List[property].limit){
                filledAttributeCount++
            }
            totalAttributeCount++
        }
        if (totalAttributeCount === filledAttributeCount){
            
            getCities()
        }
        
    }, [attributeInfo_List])




    //posts to the backend to get recommended cities
    const getCities = () => {
        //TODO create code to get cities
        //Will need to create new state variable for it
        // will need to replace the information object on the stack
        const targetBackendURL = 'http://localhost:8000/recommendCities/'
        const options = {
            method: "POST",
            mode: 'cors',
            headers: {
                "Content-Type": "application/json",
                "Access-Control-Allow-Origin": "*"
            },
            body: JSON.stringify(attributeInfo_List)
        }

        fetch(targetBackendURL, options)
            .then((response) => {
                return response.json();
            })
            .then((data) => {
                setCitiesList(data)
                setTripInfoIsFull(true)
            })
            .catch((error) => console.log(error));
        return null
    }



    

    return <>
    <div class='container mt-4'> 
        <div class="row">
            <div class='col-md-3' style={{height: "860px", overflow: "auto" }}>      
                    <Information 
                    activitiesInfo={attributeInfo_List}
                    tripFull={tripInfoIsFull}
                    citiesInfo={citiesObject}
                    showLeftColumn={showCitiesLeftColumn}
                    setShowLeftColumn={setShowCitiesLeftColumn}
                    />
                    
                 
            </div>
            <div class='col-md-9' >
                <div class='card'>
                    <Chat
                    attributeInfoList={attributeInfo_List}
                    setAttributeInfoList={setAttributeInfo_List} 
                    userId={userId}
                    /> 
                </div>
            </div>
        </div>
        <div class="row mt-2 row-cols-1 row-cols-md-4 g-4">
            {!showCitiesLeftColumn &&
               <CitiesContainer
                    citiesInfo={citiesObject}
                    tripFull={tripInfoIsFull}
                    /> 
            }
        </div>
    </div>
    </>

}
export default Main