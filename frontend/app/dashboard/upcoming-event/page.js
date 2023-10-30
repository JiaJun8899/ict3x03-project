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
  Text,
  Button,
  Box,
  Heading,
  Image,
  Input,
  FormControl,
} from "../../providers"
import NextLink from "next/link";
import React, { useState, useEffect } from "react";
import { DateTime } from "luxon";
import axios from "axios";
import { API_HOST } from "@/app/utils/utils";
import Cookie from "js-cookie";
// import { Providers } from "@/app/providers";

function Feature({ title, desc, ...rest }) {
  return (
    <Box p={5} shadow="md" borderWidth="1px" {...rest}>
      <Heading fontSize="xl">{title}</Heading>
      <Text mt={4}>{desc}</Text>
    </Box>
  );
}

function StackEx() {
  return (
    <Stack m={8} direction="row">
      <Feature
        title="Plan Money"
        desc="The future can be even brighter but a goal without a plan is just a wish"
      />
      <Feature
        title="Save Money"
        desc="You deserve good things. With a whooping 10-15% interest rate per annum, grow your savings on your own terms with our completely automated process"
      />
    </Stack>
  );
}

function EventRow({ event, index }) {
  // console.log(event);
  const startDate = DateTime.fromISO(event.startDate)
    .toJSDate()
    .toLocaleString("en-SG");
  const endDate = DateTime.fromISO(event.endDate)
    .toJSDate()
    .toLocaleString("en-SG");
  return (
    <Tr>
      <Td>
        <Image
          src={
            event.eventImage
              ? "http://localhost:8000" + event.eventImage
              : "https://picsum.photos/200"
          }
        />
      </Td>
      {/* <Td>{event.organizer}</Td> */}
      <Td>{event.eventName}</Td>
      <Td>{startDate}</Td>
      <Td>{endDate}</Td>
      <Td>{event.eventStatus}</Td>
      <Td>
        <NextLink href={`/dashboard/event?eid=${event.eid}`}>
          <Button variant={"link"}>Details</Button>
        </NextLink>
      </Td>
    </Tr>
  );
}

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
    console.log(response.data);
  } catch (error) {
    console.log(error);
  }
}

export default function Page(props) {
  // var allEvents = props.data;
  // const setEvent  = (event)=>{
  //   props.callback(event)
  // }
  const [events, setEvents] = useState([]);
  async function getAllData() {
    try {
      const response = await axios.get(`${API_HOST}/get-upcoming-events/`,
      {withCredentials:true});
      console.log(response);
      setEvents(response.data);
      
    } catch (error) {
      console.log(error);
    }
  }
  useEffect(() => {
    getAllData();
  }, []);
  const [searchText, setSearchText] = useState("");
  function CreateEventRow() {
    return events.map((event, index) => {
      return <EventRow event={event} key={index} />;
    });
  }
  return (
    <>
      <StackEx />
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
      <Stack>
        <TableContainer spacing={8} mx={8} shadow="md" borderWidth="1px">
          <Heading fontSize="xl" p={5}>
            Events to join
          </Heading>
          <Table variant="simple" size="sm">
            <Thead>
              <Tr>
                <Th>Image</Th>
                {/* <Th>Organiser</Th> */}
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
