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
  useToast,
} from "../providers";
import React from "react";
import NextLink from "next/link";
import { useRouter } from "next/navigation";
import { useEffect, useState } from "react";
import axios from "axios";
import { API_HOST, API_IMAGE, convertTime } from "@/app/utils/utils";
import Cookie from "js-cookie";

export default function OrganiserDashboard() {
  const [allEvents, setAllEvents] = useState([]);
  const router = useRouter();
  const toast = useToast();
  async function getEvents() {
    try {
      const response = await axios.get(`${API_HOST}/get-event-byorg/`, {
        withCredentials: true,
      });
      setAllEvents(response.data);
    } catch (error) {
      toast({
        title: "Failed to get events.",
        status: "error",
        duration: 3000,
        isClosable: true,
      });
    }
  }
  function Feature({ title, desc }) {
    return (
      <Box p={5} shadow="md" borderWidth="1px">
        <Heading fontSize="xl">{title}</Heading>
        <Text mt={4}>{desc}</Text>
        <Button
          onClick={() => {
            router.push("/dashboard/create-event");
          }}
        >
          Create Event Page
        </Button>
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
      </Stack>
    );
  }
  function CreateEventRow() {
    return allEvents.map((event, index) => {
      return <EventRow event={event.event} key={index} />;
    });
  }
  async function deleteEvent(eId) {
    try {
      await axios.delete(API_HOST + "/get-event-byorg/", {
        data: {
          eid: eId,
        },
        headers: {
          "X-CSRFToken": Cookie.get("csrftoken"),
        },
        withCredentials: true,
      });
      toast({
        title: "Event Deleted",
        status: "success",
        duration: 3000,
        isClosable: true,
      });
      router.refresh();
    } catch (error) {
      toast({
        title: "Event failed to Deleted",
        status: "error",
        duration: 3000,
        isClosable: true,
      });
    }
  }

  function DeleteModal(eventData) {
    const { isOpen, onOpen, onClose } = useDisclosure();
    const event = eventData.eventData;
    return (
      <>
        <Link onClick={onOpen}>Delete Event</Link>
        <Modal isOpen={isOpen} onClose={onClose}>
          <ModalOverlay />
          <ModalContent>
            <ModalHeader>Delete Event Modal</ModalHeader>
            <ModalCloseButton />
            <ModalBody>
              Are you sure you want to delete {event.eventName}?
            </ModalBody>
            <ModalFooter>
              <Button
                colorScheme="red"
                mr={3}
                onClick={() => {
                  onClose();
                  deleteEvent(event.eid);
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
          <Link
            as={NextLink}
            href={"/dashboard/edit-event/?event=" + event.eid}
            prefetch={false}
          >
            Edit
          </Link>
          | <DeleteModal eventData={event} />|{" "}
          <Link
            as={NextLink}
            href={"/dashboard/view-event/?event=" + event.eid}
            prefetch={false}
          >
            View Details
          </Link>
        </Td>
      </Tr>
    );
  }
  useEffect(() => {
    getEvents();
  }, []);
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
