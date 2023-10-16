import { getEventsByID } from "@/app/utils/utils";
import ViewEventDetails from "../ViewEvent";
// This part is important!
export const dynamic = "force-dynamic";

export default async function Page({ params, searchParams }) {
  const eventSolo = await getEventsByID(params.eid, searchParams.event);
  console.log(eventSolo);
  return (
    <>
      <ViewEventDetails eventData={eventSolo} />
    </>
  );
}