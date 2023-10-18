"use client";
import {
  Table,
  Thead,
  Tbody,
  Tfoot,
  Tr,
  Th,
  Td,
  TableCaption,
  TableContainer,
  Stack,
  Text,
  Button,
  Box,
  Heading,
  Image,
  Input,
  FormControl,
} from "../providers";
import NextLink from "next/link";
import React, { useState, useEffect } from "react";
import { DateTime } from "luxon";
import axios from "axios";

let _csrfToken = null;
const API_HOST = "http://localhost:8000/api";

async function getCsrfToken() {
  if (_csrfToken === null) {
    const response = await fetch(`${API_HOST}/csrf/`, {
      credentials: "include",
    });
    const data = await response.json();
    _csrfToken = data.csrfToken;
  }
  return _csrfToken;
}

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
        <Image src="https://picsum.photos/200" />
      </Td>
      {/* <Td>{event.organizer}</Td> */}
      <Td>{event.eventName}</Td>
      <Td>{startDate}</Td>
      <Td>{endDate}</Td>
      <Td>{event.eventStatus}</Td>
      <Td>
        <NextLink href={`event?eid=${event.eid}`}>
          <Button variant={"link"}>Details</Button>
        </NextLink>
      </Td>
    </Tr>
  );
}

async function submitSearch(x, setAllEvents) {
  const token = await getCsrfToken();
  console.log(x);
  try {
    const response = await axios.post(
      `${API_HOST}/search-events/`,
      { name: x },
      {
        withCredentials: true,
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": token,
        },
      }
    );
    setAllEvents(response.data);
    console.log(response.data);
  } catch (error) {
    console.log(error);
  }
}

export default function RegularDashboard(props) {
  // var allEvents = props.data;
  // const setEvent  = (event)=>{
  //   props.callback(event)
  // }
  const [events, setEvents] = useState([]);
  async function getAllData() {
    try {
      const API_HOST = "http://localhost:8000/api";
      const response = await axios.get(`${API_HOST}/get-all-events/`);
      setEvents(response.data);
      // console.log(response);
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
