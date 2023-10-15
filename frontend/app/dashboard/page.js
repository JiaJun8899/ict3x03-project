import { Suspense } from "react";
import { getUser, getEvents, getEventsOrg } from "../utils/utils";
import OrganiserDashboard from "./organiserDashboard";
import RegularDashboard from "./normalUserDashboard";

export const dynamic = "force-dynamic";

async function Dashboard({ promise }) {
  const userRole = await promise;
  if (userRole.role != "test") {
    const data = await getEvents();
    return <RegularDashboard data={data} />;
  } else {
    const orgID = "2364004d84ce4462b27f6ef43e5529f5";
    const data = await getEventsOrg(orgID);
    console.log("got fetch?")
    console.log(data)
    return <OrganiserDashboard data={data} />;
  }
}

export default async function Page() {
  const userRole = getUser();
  return (
    <div>
      <Suspense fallback={<p>Loading ...</p>}>
        <Dashboard promise={userRole} />
      </Suspense>
    </div>
  );
}
