'use client'
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
} from "../providers";
import React from "react";
import { DateTime } from "luxon";

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

function EventRow({event, index}){
  const startDate = DateTime.fromISO(event.event.startDate)
    .toJSDate()
    .toLocaleString("en-SG");
  const endDate = DateTime.fromISO(event.event.endDate)
    .toJSDate()
    .toLocaleString("en-SG");
  return (
    <Tr>
      <Td>
        <Image src="https://picsum.photos/200" />
      </Td>
      <Td>{event.organizer}</Td>
      <Td>{event.event.eventName}</Td>
      <Td>{startDate}</Td>
      <Td>{endDate}</Td>
      <Td>{event.event.eventStatus}</Td>
      <Td><Button>Do something</Button></Td>
    </Tr>
  );
}

export default function RegularDashboard(props) {
  const allEvents = props.data
  function CreateEventRow() {
    return allEvents.map((event, index) => {
      return <EventRow event={event} key={index} />;
    });
  }
  return (
    <>
      <StackEx />
      <Stack>
        <TableContainer spacing={8} mx={8} shadow="md" borderWidth="1px">
          <Heading fontSize="xl" p={5}>
            Events to join
          </Heading>
          <Table variant="simple" size="sm">
            <Thead>
              <Tr>
                <Th>Image</Th>
                <Th>Organiser</Th>
                <Th>Event Name</Th>
                <Th>Start Date</Th>
                <Th>End Date</Th>
                <Th>Status</Th>
                <Th>Action</Th>
              </Tr>
            </Thead>
            <Tbody>
              {CreateEventRow()}
            </Tbody>
          </Table>
        </TableContainer>
      </Stack>
    </>
  );
}
