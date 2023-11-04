"use client";

import {
  Box,
  Container,
  Stack,
  Text,
  Image,
  Flex,
  VStack,
  Heading,
  SimpleGrid,
  StackDivider,
  useColorModeValue,
  List,
  ListItem,
  Link,
  Button,
  ButtonGroup,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalFooter,
  ModalBody,
  ModalCloseButton,
  useDisclosure,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  TableContainer,
} from "@chakra-ui/react";
import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import axios from "axios";
import { API_HOST, API_IMAGE, convertTime } from "@/app/utils/utils";
import Cookie from "js-cookie";

async function deleteEvent(eId) {
  try {
    await axios.delete(API_HOST + "/get-event-byorg/", {
      data: {
        eid: eId,
      },
      headers: {
        "Content-Type": "application/json",
        "X-CSRFToken": Cookie.get("csrftoken"),
      },
      withCredentials: true,
    });
  } catch (error) {
    console.error("There was an issue deleting the event")
  }
}
function DeleteModal(eventData) {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const event = eventData.eventData;
  const router = useRouter();
  return (
    <>
      <Button colorScheme="red" onClick={onOpen}>
        Delete Event
      </Button>
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
                deleteEvent(event.eid);
                onClose();
                router.replace("/dashboard", { replace: true });
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

function ParticpantRow({ particpant, index }) {
  const userInfo = particpant.participant.user;
  return (
    <Tr>
      <Td>{userInfo.first_name}</Td>
      <Td>{userInfo.last_name}</Td>
      <Td>{userInfo.phoneNum}</Td>
      <Td>{userInfo.email}</Td>
    </Tr>
  );
}

function CreateEventRow(participantData) {
  return participantData.map((particpant, index) => {
    return <ParticpantRow particpant={particpant} key={index} />;
  });
}

function ViewParticipantModal(participantData) {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const participantList = participantData.participantData;
  return (
    <>
      <Button variant={"ghost"} onClick={onOpen}>
        View Participants List
      </Button>
      <Modal isOpen={isOpen} onClose={onClose} size={"full"}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Particpant List</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <TableContainer spacing={8} mx={8} shadow="md" borderWidth="1px">
              <Table variant="simple" size="sm">
                <Thead>
                  <Tr>
                    <Th>First Name</Th>
                    <Th>Last Name</Th>
                    <Th>Phone Number</Th>
                    <Th>Email</Th>
                  </Tr>
                </Thead>
                <Tbody>{CreateEventRow(participantList)}</Tbody>
              </Table>
            </TableContainer>
          </ModalBody>
          <ModalFooter>
            <Button colorScheme="blue" onClick={() => onClose()}>
              Close
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </>
  );
}

export default function ViewEventDetails({ eventID }) {
  const [event, setEvent] = useState({
    eventName: "",
    startDate: "",
    endDate: "",
    noVol: "",
    eventDesc: "",
    eventImage: undefined,
  });
  const [participant, setParticipants] = useState([]);
  const router = useRouter();
  async function getEvent() {
    try {
      const response = await axios.get(
        `${API_HOST}/get-single-event/${eventID}`,
        {
          withCredentials: true,
        }
      );
      setEvent(response.data);
    } catch (error) {
      console.error("There was an fetching your profile", error);
    }
  }

  async function getParticpants() {
    try {
      const response = await axios.get(
        `${API_HOST}/view-participants/${eventID}`,
        {
          withCredentials: true,
        }
      );
      setParticipants(response.data);
    } catch (error) {
      console.error("There was an fetching your profile", error);
    }
  }

  useEffect(() => {
    getEvent();
    getParticpants();
  }, [eventID]);

  return (
    <Container maxW={"7xl"}>
      <SimpleGrid
        columns={{ base: 1, lg: 2 }}
        spacing={{ base: 8, md: 10 }}
        py={{ base: 18, md: 24 }}
      >
        <Flex>
          <Image
            rounded={"md"}
            alt={"product image"}
            src={
              event.eventImage
                ? API_IMAGE + event.eventImage
                : "https://picsum.photos/200"
            }
            fit={"cover"}
            align={"center"}
            w={"100%"}
            h={{ base: "100%", sm: "400px", lg: "500px" }}
          />
        </Flex>
        <Stack spacing={{ base: 6, md: 10 }}>
          <Box as={"header"}>
            <Heading
              lineHeight={1.1}
              fontWeight={600}
              fontSize={{ base: "2xl", sm: "4xl", lg: "5xl" }}
            >
              {event.eventName}
            </Heading>
          </Box>

          <Stack
            spacing={{ base: 4, sm: 6 }}
            direction={"column"}
            divider={
              <StackDivider
                borderColor={useColorModeValue("gray.200", "gray.600")}
              />
            }
          >
            <VStack spacing={{ base: 4, sm: 6 }} align={["left"]}>
              <Text
                color={useColorModeValue("gray.500", "gray.400")}
                fontSize={"2xl"}
                fontWeight={"300"}
              >
                Event Description
              </Text>
              <Text fontSize={"lg"}>{event.eventDesc}</Text>
            </VStack>
            <Box>
              <Text
                fontSize={{ base: "16px", lg: "18px" }}
                color={useColorModeValue("yellow.500", "yellow.300")}
                fontWeight={"500"}
                textTransform={"uppercase"}
                mb={"4"}
              >
                Event Details
              </Text>

              <List spacing={2}>
                <ListItem>
                  <Text as={"span"} fontWeight={"bold"}>
                    Start Date:
                  </Text>{" "}
                  {convertTime(event.startDate)}
                </ListItem>
                <ListItem>
                  <Text as={"span"} fontWeight={"bold"}>
                    End Date:
                  </Text>{" "}
                  {convertTime(event.endDate)}
                </ListItem>
                <ListItem>
                  <Text as={"span"} fontWeight={"bold"}>
                    Number of Volunteers Needed:
                  </Text>{" "}
                  {event.noVol}{" "}
                  <ViewParticipantModal participantData={participant} />
                </ListItem>
                <ListItem>
                  <Text as={"span"} fontWeight={"bold"}>
                    Event Status:
                  </Text>{" "}
                  {event.eventStatus}
                </ListItem>
                <ButtonGroup>
                  <Button
                    onClick={() =>
                      router.push("/dashboard/edit-event/?event=" + eventID)
                    }
                  >
                    Edit Event
                  </Button>
                  <DeleteModal eventData={event} />
                </ButtonGroup>
              </List>
            </Box>
          </Stack>
        </Stack>
      </SimpleGrid>
    </Container>
  );
}
