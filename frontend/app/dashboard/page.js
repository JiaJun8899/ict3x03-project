import axios from "axios";
import dynamic from "next/dynamic";
import { Suspense } from "react";

const OrganiserDashboard = dynamic(() => import("./organiserDashboard"), {
  ssr: false,
});
const RegularDashboard = dynamic(() => import("./normalUserDashboard"), {
  ssr: false,
});

async function getUser() {
  const response = await axios.get("http://127.0.0.1:8000/api/test");
  return response.data;
}

async function Dashboard({ promise }) {
  const userRole = await promise;

  if (userRole.role === "test") {
    return <OrganiserDashboard />;
  } else {
    return <RegularDashboard />;
  }
}

export default async function Page() {
  const userRole = getUser();
  return (
    <div>
      <Suspense fallback={<p>Loading ...</p>}>
        <Dashboard promise={userRole} />;
      </Suspense>
    </div>
  );
}
