"use client";
import { Suspense } from "react";
import { useEffect, useState } from "react";
import dynamic from "next/dynamic";
import axios from "axios";

const API_HOST = "http://localhost:8000/api";

const OrganiserDashboard = dynamic(() => import("./organiserDashboard"), {
  ssr: false,
});
const RegularDashboard = dynamic(() => import("./normalUserDashboard"), {
  ssr: false,
});


export default function Page() {
  const [userRole, setUserRole] = useState("none");
  async function getRole() {
    try {
      const response = await axios.get(`${API_HOST}/test`, {
        withCredentials: true,
      });
      setUserRole(response.data);
    } catch (error) {
      console.error("There was an fetching your profile", error);
    }
  }
  function Dashboard() {
    const role = userRole.role;
    console.log(role);
    if (role == "Organizer") {
      return <OrganiserDashboard />;
    } else {
      return <RegularDashboard />;
    }
  }
  useEffect(() => {
    getRole();
  }, []);

  return (
    <div>
      <Suspense fallback={<p>Loading ...</p>}>
        <Dashboard userRole={userRole} />
      </Suspense>
    </div>
  );
}
