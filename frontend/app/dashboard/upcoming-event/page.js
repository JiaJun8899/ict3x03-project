"use client";
import {
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  TableContainer,
  Stack,
  Button,
  Heading,
  Image,
  Input,
  FormControl,
  useToast,
} from "../../providers";
import NextLink from "next/link";
import React, { useState, useEffect, Suspense } from "react";
import axios from "axios";
import { API_HOST, getRole, API_IMAGE, convertTime } from "@/app/utils/utils";
import { notFound } from "next/navigation";
import Cookie from "js-cookie";

function EventRow({ event, index }) {
  return (
    <Tr>
      <Td>
        <Image
          src={
            event.eventImage
              ? API_IMAGE + event.eventImage
              : "https://picsum.photos/200"
          }
        />
      </Td>
      <Td>{event.eventName}</Td>
      <Td>{convertTime(event.startDate)}</Td>
      <Td>{convertTime(event.endDate)}</Td>
      <Td>{event.eventStatus}</Td>
      <Td>
        <NextLink href={`/dashboard/event?eid=${event.eid}`}>
          <Button variant={"link"}>Details</Button>
        </NextLink>
      </Td>
    </Tr>
  );
}

export default function Page() {
  const toast = useToast();
  const [userRole, setUserRole] = useState("none");
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    getRole(setUserRole, setLoading);
  }, []);
  async function submitSearch(searchText, setAllEvents) {
    try {
      const response = await axios.post(
        `${API_HOST}/search-events/`,
        { name: searchText },
        {
          withCredentials: true,
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": Cookie.get("csrftoken"),
          },
        }
      );
      setAllEvents(response.data);
    } catch (error) {
      toast({
        title: "Searching failed.",
        status: "error",
        duration: 3000,
        isClosable: true,
      });
    }
  }

  function UpcomingEvent() {
    const role = userRole.role;
    if (role !== "Normal") {
      return notFound();
    }
    const [events, setEvents] = useState([]);
    async function getAllData() {
      try {
        const response = await axios.get(`${API_HOST}/get-upcoming-events/`, {
          withCredentials: true,
        });
        setEvents(response.data);
      } catch (error) {
        toast({
          title: "Failed to get upcoming events",
          status: "error",
          duration: 3000,
          isClosable: true,
        });
      }
    }

    useEffect(() => {
      getAllData();
    }, []);
    const [searchText, setSearchText] = useState("");
    function CreateEventRow() {
      return events.map((event, index) => {
        if (event.event) {
          return <EventRow event={event.event} key={index} />;
        } else {
          return <EventRow event={event} key={index} />;
        }
      });
    }
    return (
      <>
        <Stack m={8} direction="row">
          <FormControl id="search">
            <Input
              width="90%"
              placeholder="Search"
              value={searchText}
              onChange={(e) => setSearchText(e.target.value)}
            />
            <Button
              width="10%"
              onClick={() => submitSearch(searchText, setEvents)}
            >
              Search
            </Button>
          </FormControl>
        </Stack>
        <Stack m={8} direction={"row"}>
          <NextLink href={`/dashboard`}>
            <Button variant={"link"}>Dashboard</Button>
          </NextLink>
          <NextLink href={`/dashboard/past-event/`}>
            <Button variant={"link"}>Past Events</Button>
          </NextLink>
        </Stack>
        <Stack>
          <TableContainer spacing={8} mx={8} shadow="md" borderWidth="1px">
            <Heading fontSize="xl" p={5}>
              Events to join
            </Heading>
            <Table variant="simple" size="sm">
              <Thead>
                <Tr>
                  <Th>Image</Th>
                  <Th>Event Name</Th>
                  <Th>Start Date</Th>
                  <Th>End Date</Th>
                  <Th>Status</Th>
                  <Th>Action</Th>
                </Tr>
              </Thead>
              <Tbody>{CreateEventRow()}</Tbody>
            </Table>
          </TableContainer>
        </Stack>
      </>
    );
  }

  return (
    <div>
      <Suspense fallback={<p>Loading ...</p>}>
        {loading ? (
          <p>Building dashboard...</p>
        ) : (
          <UpcomingEvent userRole={userRole} />
        )}
      </Suspense>
    </div>
  );
}
