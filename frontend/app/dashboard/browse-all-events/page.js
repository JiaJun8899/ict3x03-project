"use client";
import { Suspense, useEffect, useState } from "react";
// import { getUser, getEvents, getEventsOrg } from "../utils/utils";
// import OrganiserDashboard from "./organiserDashboard";
import RegularDashboard from "../normalUserDashboard";
import axios from "axios";
// import { setServers } from "dns";

// export const dynamic = "force-dynamic";

async function Dashboard({data}) {
  //   const userRole = await promise;
  // const datatopass = await data;
  console.log(data)
  return <RegularDashboard data={data} />;
}

export default function Page() {
  const [events, setEvents] = useState([])
  async function getAllData() {
    try {
      const API_HOST = "http://localhost:8000/api";
      const response = await axios.get(`${API_HOST}/get-all-events/`);
      setEvents(response.data)
      // console.log(response);
    } catch (error) {
      console.log(error);
    }
  }
  useEffect(() => {
    getAllData();
  },[]);
  // const userRole = getUser();
  return (
    <div>     
       <Suspense fallback={<p>Loading ...</p>}>
        <RegularDashboard data={events} callback={setEvents} />
        </Suspense> 
    </div>
  );
}
