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
} from "@chakra-ui/react";
import React, { useState } from "react";
import axios from "axios";
import { useRouter } from "next/navigation";
import { API_HOST } from "@/app/utils/utils";
import Cookie from "js-cookie"

export default function SignupCard() {
  const router = useRouter();
  const [form, setForm] = useState({
    eventName: "",
    startDate: "",
    endDate: "",
    noVol: "",
    eventDesc: "",
    eventImage: undefined,
  });

  function updateForm(value) {
    return setForm((prev) => {
      console.log(form);
      return { ...prev, ...value };
    });
  }

  async function onSubmit(e) {
    await axios
      .post(`${API_HOST}/get-event-byorg/`, form, {
        headers: {
          "Content-Type": "multipart/form-data",
          "X-CSRFToken": Cookie.get("csrftoken"),
        },
        withCredentials: true,
      })
      .then((res) => {
        console.log(res);
      })
      .catch((error) => {
        console.log(error);
      });
    router.replace("/dashboard");
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
            Sign up
          </Heading>
          <Text fontSize={"lg"} color={"gray.600"}>
            to enjoy all of our cool features ✌️
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
                      updateForm({ eventName: e.target.value });
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
                      updateForm({ noVol: e.target.value });
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
                      updateForm({ startDate: e.target.value });
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
                      updateForm({ endDate: e.target.value });
                    }}
                  />
                </FormControl>
              </Box>
            </HStack>
            <FormControl id="email" isRequired>
              <FormLabel>Event Image</FormLabel>
              <Input
                type="file"
                accept="image/png, image/jpeg"
                onChange={(e) => {
                  updateForm({ eventImage: e.target.files[0] });
                }}
              />
            </FormControl>
            <FormControl id="eventDesc" isRequired>
              <FormLabel>Event Description</FormLabel>
              <Input
                type="text"
                value={form.eventDesc}
                onChange={(e) => {
                  updateForm({ eventDesc: e.target.value });
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
