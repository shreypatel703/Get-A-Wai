import "react-chat-elements/dist/main.css";
import { MessageBox} from "react-chat-elements";
import { FontAwesomeIcon } from '@fortawesome/react-fontawesome'
import React, { useState} from 'react';


function Chat({attributeInfoList, setAttributeInfoList, userId}) {
  const [text_entry, setText_entry] = useState('')
  const [message_list, setMessage_list] = useState([<MessageBox
    position={"left"}
    type={"text"}
    title={"Get-A-wAI Bot"}
    text="Welcome to Get-A-WAI! What do you like to do?"/>])

  const [slot_tracker, setSlot_tracker] = useState({
    "liked_activity_1": false,
    "liked_activity_2": false,
    "liked_activity_3": false,
    "preferred_climate": false,
    "preferred_travel_method": false,
    "preferred_trip_length": false,
    "preferred_budget": false,
    "user_city": false,
    "user_state": false
  })

  const handleSubmit= () => {
    setMessage_list(prev_list => [...prev_list,
          <MessageBox
            position={"right"}
            type={"text"}
            title={"Me"}
            text={text_entry}
          />
    ])
    // TODO: Change to correct RASA route
    const path1 = 'http://localhost:5005/webhooks/rest/webhook'

    const options = {
      method: "POST",
      credentials: "same-origin",
      headers: {
        "Content-Type": "application/json"
      },
      body: JSON.stringify({message: text_entry, sender: userId})
    }
  
    fetch(path1, options)
      .then((response) => {
        return response.json();
      })
      .then((data) => {
        console.log(data)
        generateTextResponse(data)
        handleResponse()
      })  
      .catch((error) => console.log(error));
      setText_entry('');
  };

  //intent type needs to match the names declared in main.js for the attrivuteInfo object
  const handleResponse = () => {

    const get_slots_url = `http://localhost:5005/conversations/${userId}/tracker`
    fetch(get_slots_url, {credentials: "same-origin"})
      .then((response2) => {
        return response2.json();
      })
      .then((tracker) => {
        console.log(tracker)
        for (const key in tracker.slots){
          console.log(`the value of key is ${key}. The value of slots tracker is ${slot_tracker[key]} The set value of the slot is ${tracker.slots[key] !== null}`)
          if (key in slot_tracker && tracker.slots[key] !== null && !slot_tracker[key]){
            add_value_to_attribute_list(key, tracker.slots)
          }
        }
      })

  }

  const add_value_to_attribute_list = (key, slots) => {

    switch (key) {
      case "liked_activity_1":
        update_activity_display(key, slots, "activities")
        break;
      case "liked_activity_2":
        update_activity_display(key, slots, "activities")
        break;
      case "liked_activity_3":
        update_activity_display(key, slots, "activities")
        break;
      case "preferred_climate":
        update_activity_display(key, slots, "climate")
        break;
      case "preferred_travel_method":
        update_activity_display(key, slots, "travelMethod")
        break;
      case "preferred_trip_length":
        update_activity_display(key, slots, "tripDuration")
        break;
      case "preferred_budget":
        update_activity_display(key, slots, "budget")
        break;
      case "user_city":
        update_activity_display(key, slots, "location")
        break;
      case "user_state":
        update_activity_display(key, slots, "location")
        break;
      default:
    }
    
  }

  const update_activity_display = (key, slots, attributeName) => {
    let updated_info = attributeInfoList
        updated_info[attributeName].list = [...updated_info[attributeName].list, slots[key]]
        console.log(updated_info)
        setAttributeInfoList({...updated_info})
        let updated_slot_tracker = slot_tracker
        updated_slot_tracker[key] = true
        setSlot_tracker({...updated_slot_tracker})
  }


  const generateTextResponse = (data) => {
      console.log(data.text)
      let adding_msg_array = []
      data.forEach(element => {
        adding_msg_array.push(<MessageBox
          position={"left"}
          type={"text"}
          title={"GET-a-wAI Bot"}
          text={element.text}/>)
      });

      setMessage_list(prev_list => [...prev_list, 
        ...adding_msg_array])
  } 


  const handleKeyDown = (event) => {
    if (event.key === 'Enter') {
      handleSubmit()
    }
  }

 
  return (
    <>
    <div class='card-body p-4' style={{height: "800px", overflow: "auto" }}>
      <div>
          {message_list.map((text_list_item,index) =>{
            return <div key={index}> {text_list_item} </div>
          })}
      </div>
    </div>
        

    <div class='card-footer bg-transparent position-relative w-100 bottom-0 m-0 p-1'>
      <div class="input-group">
        <input type="text" class="form-control border-0" placeholder="Write a message" name="user_question" value={text_entry}  onChange={e => setText_entry(e.target.value)} onKeyDown={handleKeyDown}/>
        <div class="input-group-text bg-transparent border-0">
            <button class="btn btn-light" onClick={handleSubmit} ><FontAwesomeIcon icon={"fa fa-paper-plane"} /> </button>
        </div>
      </div>
          
       
    </div>
  </>
  );
}
export default Chat