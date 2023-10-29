"use client";
import { Suspense } from "react";
import { useEffect, useState } from "react";
import dynamic from "next/dynamic";
import axios from "axios";
import { notFound } from "next/navigation";
import { API_HOST } from "@/app/utils/utils";

const CreateEvent = dynamic(() => import("./EventForm"), {
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
      console.log(response.data);
      setUserRole(response.data);
    } catch (error) {
      console.error("There was an fetching your profile", error);
    } finally {
      setLoading(false);
    }
  }
  function CreateForm() {
    const role = userRole.role;
    console.log(role);
    if (role === "Organizer") {
      return <CreateEvent />;
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
          <p>Build dashboard...</p>
        ) : (
          <CreateForm/>
        )}
      </Suspense>
    </div>
  );
}
