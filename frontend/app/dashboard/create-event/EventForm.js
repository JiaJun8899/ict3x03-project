"use client";

import {
  Flex,
  Box,
  FormControl,
  FormLabel,
  Input,
  HStack,
  Stack,
  Button,
  Heading,
  Text,
  useColorModeValue,
  useToast,
} from "@chakra-ui/react";
import React, { useState } from "react";
import axios from "axios";
import { useRouter } from "next/navigation";
import { API_HOST, updateForm } from "@/app/utils/utils";
import Cookie from "js-cookie";

export default function SignupCard() {
  const toast = useToast();
  const router = useRouter();
  const [form, setForm] = useState({
    eventName: "",
    startDate: "",
    endDate: "",
    noVol: "",
    eventDesc: "",
    eventImage: undefined,
  });

  async function onSubmit(e) {
    try {
      await axios.post(`${API_HOST}/get-event-byorg/`, form, {
        headers: {
          "Content-Type": "multipart/form-data",
          "X-CSRFToken": Cookie.get("csrftoken"),
        },
        withCredentials: true,
      });
      toast({
        title: "Event Created",
        status: "success",
        duration: 3000,
        isClosable: true,
      });
      router.replace("/dashboard");
    } catch (error) {
      if ("response" in error) {
        const values = Object.values(error.response.data);
        if (values[0] != "<") {
          toast({
            title: "Event Creation Failed",
            description: values[0],
            status: "error",
            duration: 3000,
            isClosable: true,
          });
        }
      } else {
        toast({
          title: "Event Creation Failed",
          description: "An error occured. Please try again",
          status: "error",
          duration: 3000,
          isClosable: true,
        });
      }
    }
  }
  return (
    <Flex
      minH={"100vh"}
      align={"center"}
      justify={"center"}
      bg={useColorModeValue("gray.50", "gray.800")}
    >
      <Stack spacing={8} mx={"auto"} py={12} px={6}>
        <Stack align={"center"}>
          <Heading fontSize={"4xl"} textAlign={"center"}>
            Create Volunteering Event
          </Heading>
          <Text fontSize={"lg"} color={"gray.600"}>
            Create an exciting volunteering event for everyone! ✌️
          </Text>
        </Stack>
        <Box
          rounded={"lg"}
          bg={useColorModeValue("white", "gray.700")}
          boxShadow={"lg"}
          p={8}
        >
          <Stack spacing={4}>
            <HStack>
              <Box>
                <FormControl id="eventName" isRequired>
                  <FormLabel>Event Name</FormLabel>
                  <Input
                    type="text"
                    value={form.eventName}
                    onChange={(e) => {
                      updateForm({ eventName: e.target.value }, setForm);
                    }}
                  />
                </FormControl>
              </Box>
              <Box>
                <FormControl id="noVol" isRequired>
                  <FormLabel>Volunteers Needed</FormLabel>
                  <Input
                    type="number"
                    value={form.noVol}
                    onChange={(e) => {
                      updateForm({ noVol: e.target.value }, setForm);
                    }}
                  />
                </FormControl>
              </Box>
            </HStack>
            <HStack>
              <Box>
                <FormControl id="startDate" isRequired>
                  <FormLabel>Start Date</FormLabel>
                  <Input
                    type="datetime-local"
                    min={new Date().toISOString().substring(0, 16)}
                    value={form.startDate}
                    onChange={(e) => {
                      updateForm({ startDate: e.target.value }, setForm);
                    }}
                  />
                </FormControl>
              </Box>
              <Box>
                <FormControl id="endDate">
                  <FormLabel>End Date</FormLabel>
                  <Input
                    type="datetime-local"
                    min={form.startDate}
                    value={form.endDate}
                    onChange={(e) => {
                      updateForm({ endDate: e.target.value }, setForm);
                    }}
                  />
                </FormControl>
              </Box>
            </HStack>
            <FormControl id="email" isRequired>
              <FormLabel>Event Image</FormLabel>
              <Input
                type="file"
                accept="image/png"
                onChange={(e) => {
                  updateForm({ eventImage: e.target.files[0] }, setForm);
                }}
              />
            </FormControl>
            <FormControl id="eventDesc" isRequired>
              <FormLabel>Event Description</FormLabel>
              <Input
                type="text"
                value={form.eventDesc}
                onChange={(e) => {
                  updateForm({ eventDesc: e.target.value }, setForm);
                }}
              />
            </FormControl>
            <Stack spacing={10} pt={2}>
              <Button
                loadingText="Submitting"
                size="lg"
                bg={"blue.400"}
                color={"white"}
                _hover={{
                  bg: "blue.500",
                }}
                onClick={onSubmit}
              >
                Create Event
              </Button>
            </Stack>
          </Stack>
        </Box>
      </Stack>
    </Flex>
  );
}
