"use server";
import "server-only";
import axios from "axios";

axios.defaults.baseURL = "http://backend:8000/api";
axios.defaults.headers = {
  "Cache-Control": "no-cache",
  Pragma: "no-cache",
  Expires: "0",
};
axios.defaults.timeout = 5000;
axios.defaults.withCredentials = true;

export async function getUser() {
  const response = await axios.get("test");
  console.log(response);
  return response.data;
}

export async function getEvents() {
  const response = await axios.get("get-all-events/");
  return response.data;
}

export async function getEventsOrg(orgID) {
  const response = await axios.get("get-event-byorg/" + orgID);
  return response.data;
}

export async function getEventsByID(orgID, eID) {
  const response = await axios.get("get-single-event/" + orgID + "/" + eID);
  return response.data;
}

export async function deleteEvent(eId) {
  const response = await axios.delete(
    "get-event-byorg/2364004d84ce4462b27f6ef43e5529f5/",
    {
      data: {
        eid: eId,
      },
    }
  );
  return response.data;
}

export async function registerAcc(data) {
  const response = await axios
    .post("register", data)
    .then(function (response) {
      return response.status;
    })
    .catch(function (error) {
      return error.response.status;
    });
}
