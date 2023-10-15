import { getEventsByID } from "@/app/utils/utils";
import EditEvent from "../editEvent";
// This part is important!
export const dynamic = "force-dynamic";
async function getEvent(oid, eid){
  const eventSolo = await getEventsByID(oid, eid);
  console.log(eventSolo)
  return eventSolo
}
export default async function Page({ params, searchParams }) {
  const eventSolo = await getEvent(params.oid, searchParams.event);
  return (
    <>
      <EditEvent eventData={eventSolo}/>
    </>
  )
}