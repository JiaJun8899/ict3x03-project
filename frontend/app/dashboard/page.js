"use client";
import { Suspense } from "react";
import { useEffect, useState } from "react";
import dynamic from "next/dynamic";
import axios from "axios";
import { notFound } from "next/navigation";
import { API_HOST } from "@/app/utils/utils";

const OrganiserDashboard = dynamic(() => import("./organiserDashboard"), {
  ssr: false,
});
const RegularDashboard = dynamic(() => import("./normalUserDashboard"), {
  ssr: false,
});

export default function Page() {
  const [userRole, setUserRole] = useState("none");
  const [loading, setLoading] = useState(true);
  async function getRole() {
    try {
      const response = await axios.get(`${API_HOST}/check-auth`, {
        withCredentials: true,
      });
      setUserRole(response.data);
    } catch (error) {
      console.error("There is an issue checking your auth");
    } finally {
      setLoading(false);
    }
  }
  function Dashboard() {
    const role = userRole.role;
    if (role === "Organizer") {
      return <OrganiserDashboard />;
    } else if (role === "Normal") {
      return <RegularDashboard />;
    } else {
      return notFound();
    }
  }
  useEffect(() => {
    getRole();
  }, []);

  return (
    <div>
      <Suspense fallback={<p>Loading ...</p>}>
        {loading ? (
          <p>Building dashboard...</p>
        ) : (
          <Dashboard userRole={userRole} />
        )}
      </Suspense>
    </div>
  );
}
