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
  useToast,
} from "@chakra-ui/react";
import { Suspense } from "react";
// Import only what's needed
import { useSearchParams, notFound } from "next/navigation";
import { useEffect, useState } from "react";
import axios from "axios";
import { API_HOST, convertTime, getRole, API_IMAGE } from "@/app/utils/utils";
import Cookie from "js-cookie";

const WithdrawModal = ({ eventData, cancelSignup }) => {
  const { isOpen, onOpen, onClose } = useDisclosure();
  const event = eventData;
  return (
    <>
      <Button colorScheme="red" onClick={onOpen}>
        Withdraw Event
      </Button>
      <Modal isOpen={isOpen} onClose={onClose}>
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Withdraw from event?</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            Are you sure you want to withdraw from {event.eventName}?
          </ModalBody>
          <ModalFooter>
            <Button
              colorScheme="red"
              mr={3}
              onClick={() => {
                cancelSignup();
                onClose();
              }}
            >
              Confirm Withdraw
            </Button>
            <Button colorScheme="blue" onClick={() => onClose()}>
              Close
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </>
  );
};

export default function Page() {
  const [userRole, setUserRole] = useState("none");
  const [loading, setLoading] = useState(true);
  useEffect(() => {
    getRole(setUserRole, setLoading);
  }, []);

  function Event() {
    const role = userRole.role;
    if (role !== "Organizer" && role !== "Normal") {
      return notFound();
    }
    const toast = useToast();
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

    async function fetchEvent() {
      try {
        const response = await axios.get(`${API_HOST}/get-event/${search}`, {
          withCredentials: true,
        });
        setEvent(response.data.data);
      } catch (error) {
        toast({
          title: "Unable to fetch events",
          status: "error",
          duration: 3000,
          isClosable: true,
        });
      }
    }

    const signup = async () => {
      try {
        await axios.post(
          `${API_HOST}/sign-up-event/`,
          { eid: search },
          {
            withCredentials: true,
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": Cookie.get("csrftoken"),
            },
          }
        );
        toast({
          title: "Signup successful.",
          status: "success",
          duration: 3000,
          isClosable: true,
        });
      } catch (error) {
        toast({
          title: "Signup failed.",
          status: "error",
          duration: 3000,
          isClosable: true,
        });
      }
    };
    const cancelSignup = async () => {
      try {
        await axios.delete(`${API_HOST}/cancel-sign-up-event/`, {
          withCredentials: true,
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": Cookie.get("csrftoken"),
          },
          data: { eid: search },
        });
        toast({
          title: "Withdraw successful.",
          status: "success",
          duration: 3000,
          isClosable: true,
        });
      } catch (error) {
        toast({
          title: "Withdraw failed.",
          status: "error",
          duration: 3000,
          isClosable: true,
        });
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
                        Event Status:
                      </Text>{" "}
                      {event.eventStatus}
                    </ListItem>
                    <ButtonGroup>
                      <Button onClick={signup}>Sign Up Event</Button>
                      <WithdrawModal
                        eventData={event}
                        cancelSignup={cancelSignup}
                      />
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

  return (
    <div>
      <Suspense fallback={<p>Loading ...</p>}>
        {loading ? <p>Building dashboard...</p> : <Event userRole={userRole} />}
      </Suspense>
    </div>
  );
}
