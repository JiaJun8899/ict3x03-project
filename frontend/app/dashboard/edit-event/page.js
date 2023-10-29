"use client";
import { Suspense } from "react";
import { useEffect, useState } from "react";
import dynamic from "next/dynamic";
import axios from "axios";
import { notFound } from "next/navigation";
import { API_HOST } from "@/app/utils/utils";

const CreateEvent = dynamic(() => import("./EditEventForm"), {
  ssr: false,
});

export default function Page({ searchParams }) {
  const [validEvent, setValidEvent] = useState("none");
  const [loading, setLoading] = useState(true);
  async function getValid() {
    try {
      const response = await axios.get(
        `${API_HOST}/check-valid-organizer/${searchParams.event}`,
        {
          withCredentials: true,
        }
      );
      console.log(response.data);
      setValidEvent(response.data);
    } catch (error) {
      console.error("There was an fetching your profile", error);
    } finally {
      setLoading(false);
    }
  }
  function CreateForm() {
    const valid = validEvent.valid;
    console.log(valid);
    if (valid) {
      return <CreateEvent searchParams={searchParams} />;
    } else {
      return notFound();
    }
  }
  useEffect(() => {
    getValid();
  }, []);

  return (
    <div>
      <Suspense fallback={<p>Loading ...</p>}>
        {loading ? <p>Loading...</p> : <CreateForm />}
      </Suspense>
    </div>
  );
}
