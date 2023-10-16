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
  Link,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
  useDisclosure,
} from "../providers";
import React from "react";
import { DateTime } from "luxon";
import NextLink from "next/link";
import { deleteEvent } from "../utils/utils";
import { useRouter } from "next/navigation";

function DeleteModal(eventData) {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const event = eventData.eventData
  const router = useRouter();
  return (
    <>
      <Link onClick={onOpen}>Delete Event</Link>
      <Modal isOpen={isOpen} onClose={onClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Delete Event Modal</ModalHeader>
          <ModalCloseButton />
          <ModalBody>Are you sure you want to delete {event.eventName}?</ModalBody>
          <ModalFooter>
            <Button
              colorScheme="red"
              mr={3}
              onClick={() => {
                deleteEvent(event.eid);onClose();router.refresh()
              }}
            >
              Delete Event
            </Button>
            <Button colorScheme="blue" onClick={() => onClose()}>
              Close
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </>
  );
}

function Feature({ title, desc }) {
  const router = useRouter()
  return (
    <Box p={5} shadow="md" borderWidth="1px">
      <Heading fontSize="xl">{title}</Heading>
      <Text mt={4}>{desc}</Text>
      <Button onClick={()=>{router.push('/dashboard/create-event')}}>Create Event Page</Button>
    </Box>
  );
}

function StackEx() {
  return (
    <Stack m={8} direction="row" align="stretch" alignItems="stretch">
      <Feature
        title="Create Event"
        desc="The future can be even brighter but a goal without a plan is just a wish"
      />
      <Feature
        title="Header"
        desc="Some desc"
      />
    </Stack>
  );
}

function convertTime(time) {
  const convertedTime = DateTime.fromISO(time)
    .toJSDate()
    .toLocaleString("en-SG");
  return convertedTime;
}

function EventRow({ event, index }) {

  return (
    <Tr>
      <Td>
        <Image
          src={
            event.eventImage
              ? "http://127.0.0.1:8000" + event.eventImage
              : "https://picsum.photos/200"
          }
        />
      </Td>
      <Td>{event.eventName}</Td>
      <Td>{convertTime(event.startDate)}</Td>
      <Td>{convertTime(event.endDate)}</Td>
      <Td>{event.eventStatus}</Td>
      <Td>
        <Link
          as={NextLink}
          href={
            "/dashboard/edit-event/2364004d84ce4462b27f6ef43e5529f5/?event=" +
            event.eid
          }
          prefetch={false}
        >
          Edit
        </Link>
        | <DeleteModal eventData={event} />|{" "}
        <Link
          as={NextLink}
          href={
            "/dashboard/view-event/2364004d84ce4462b27f6ef43e5529f5/?event=" +
            event.eid
          }
          prefetch={false}
        >
          View Details
        </Link>
      </Td>
    </Tr>
  );
}

export default function OrganiserDashboard(props) {
  const allEvents = props.data
  function CreateEventRow() {
    return allEvents.map((event, index) => {
      return <EventRow event={event.event} key={index} />;
    });
  }
  return (
    <>
      <StackEx />
      <Stack>
        <TableContainer spacing={8} mx={8} shadow="md" borderWidth="1px">
          <Heading fontSize="xl" p={5}>
            My Events
          </Heading>
          <Table variant="simple" size="sm">
            <Thead>
              <Tr>
                <Th>Image</Th>
                <Th>Event Name</Th>
                <Th>Start Date</Th>
                <Th>End Date</Th>
                <Th>Status</Th>
                <Th>Actions</Th>
              </Tr>
            </Thead>
            <Tbody>{CreateEventRow()}</Tbody>
          </Table>
        </TableContainer>
      </Stack>
    </>
  );
}
