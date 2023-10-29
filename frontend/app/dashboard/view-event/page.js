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
} from "@chakra-ui/react";
import React,{useState, useEffect} from "react";
import { useRouter } from "next/navigation";
import axios from "axios";
import { API_HOST, convertTime } from "@/app/utils/utils";


async function deleteEvent(eId) {
  const response = await axios.delete(API_HOST + "/get-event-byorg/", {
    data: {
      eid: eId,
    },
    withCredentials: true,
  });
  return response.data;
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

export default function ViewEventDetails({ searchParams }) {
    const [event, setEvent] = useState({
      eventName: "",
      startDate: "",
      endDate: "",
      noVol: "",
      eventDesc: "",
      eventImage: undefined,
    });
  const router = useRouter();
  async function getEvent() {
    try {
      const response = await axios.get(
        `${API_HOST}/get-single-event/${searchParams.event}`,
        {
          withCredentials: true,
        }
      );
      console.log(response.data);
      setEvent(response.data);
    } catch (error) {
      console.error("There was an fetching your profile", error);
    }
  }
  useEffect(() => {
    getEvent();
  }, [searchParams]);

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
                ? "http://localhost:8000" + event.eventImage
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
                  {event.noVol} <Link>Volunteer List</Link>
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
                      router.push(
                        "/dashboard/edit-event/?event=" + searchParams.event
                      )
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
