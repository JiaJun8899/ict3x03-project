'use server'
import "server-only"
import axios from "axios";


const URI = "http://172.18.0.4:8000/api/"

function formDataToJson(formData) {
  let json = {};
  if (!(formData instanceof FormData)) return json;
  formData.forEach((value, key) => {
    json[key] = value;
  });
  return json;
}

export async function getUser() {
  const response = await axios.get(URI + "test");
  return response.data;
}

export async function getEvents() {
  const response = await axios.get(URI + "get-all-events/");
  return response.data;
}

export async function getEventsOrg(orgID) {
  const response = await axios.get(
    URI + "get-event-byorg/" + orgID
  );
  return response.data;
}

export async function getEventsByID(orgID, eID){
  const response = await axios.get(
    URI + "get-single-event/" + orgID +"/" + eID
  );
  return response.data
}

export async function createEvent(form) {
  console.log(form.get("eventImage"));
  const response = await axios
    .post(
      "http://127.0.0.1:8000/api/get-event-byorg/2364004d84ce4462b27f6ef43e5529f5/",
      form,
      {
        headers: {
          "Content-Type": "multipart/form-data",
        },
      }
    )
    return response.data
}

export async function deleteEvent(eId) {
  const response = await axios.delete(
    "http://127.0.0.1:8000/api/get-event-byorg/2364004d84ce4462b27f6ef43e5529f5/",
    {
      data: {
        eid: eId,
      },
    }
  );
}