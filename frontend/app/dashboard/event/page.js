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
import { DateTime } from "luxon";
import ViewEventDetails from "../view-event/ViewEvent";
// Import only what's needed
import { useSearchParams, useRouter, useParams } from "next/navigation";
import { useEffect, useState } from "react";
import axios from "axios";

export const dynamic = "force-dynamic";

let _csrfToken = null;

function convertTime(time) {
  const convertedTime = DateTime.fromISO(time)
    .toJSDate()
    .toLocaleString("en-SG");
  console.log(convertedTime.substring(0, 16));
  return convertedTime;
}
const DeleteModal = ({eventData,cancelSignup}) => {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const event = eventData
  const router = useRouter();
  return (
    <>
      <Button colorScheme="red" onClick={onOpen}>
        Cancel Event
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
              onClick={cancelSignup}
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

export default function Page() {
    // Here need to check if its a normal user if not just throw 404
//   if ( 0 === 0 ){
//     return (
//         <>GG</>
//     )
//   }
  const API_HOST = "http://localhost:8000/api";
  const searchParams = useSearchParams();
  const search = searchParams.get("eid");
  const [event, setEvent] = useState({
    eid: "",
    endDate: "",
    eventDesc: "",
    eventImage: null,
    eventName: "",
    eventStatus: "",
    noVol: 0,
    startDate: "",
  });
  useEffect(() => {
    fetchEvent();
  }, []);

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

  async function fetchEvent() {
    try {
      const response = await axios.get(`${API_HOST}/get-event/${search}`);
      // console.log(response.data)
      console.log(response.data.data);
      setEvent(response.data.data);
      // return response
    } catch (error) {
      console.log(error);
    }
  }

  const signup = async () => {
    const token = await getCsrfToken();
    try {
      const response = await axios.post(
        `${API_HOST}/sign-up-event/`,
        { eid: search },
        {
          withCredentials: true,
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": token,
          },
        }
      );
      console.log(response);
    } catch (error) {
      console.log(error);
    }
  };
  const cancelSignup = async () => {
    const token = await getCsrfToken();
    // console.log('cancel signup')
    try {
        const response = await axios.delete(
            `${API_HOST}/cancel-sign-up-event/`,
            {
                withCredentials: true,
                headers: {
                    "Content-Type": "application/json",
                    "X-CSRFToken": token,
                },
                data: { eid: search },
            }
        );
        console.log(response);
    } catch (error) {
        console.error(error);
    }
};

  return (
    <>
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
                  ? "http://127.0.0.1:8000" + event.eventImage
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
                    <Button onClick={signup}>Sign Up Event</Button>
                    <DeleteModal eventData={event} cancelSignup={cancelSignup} />
                  </ButtonGroup>
                </List>
              </Box>
            </Stack>
          </Stack>
        </SimpleGrid>
      </Container>
    </>
  );
}
