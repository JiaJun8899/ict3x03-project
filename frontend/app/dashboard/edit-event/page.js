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
  useColorModeValue,
  ButtonGroup,
  Image,
} from "@chakra-ui/react";
import React, { useState, useEffect } from "react";
import axios from "axios";
import Link from "next/link";
import { API_HOST } from "@/app/utils/utils";

let _csrfToken = null;

async function onSubmit(data) {
  console.log(data);
  const token = await getCsrfToken();

  const response = await axios.put(`${API_HOST}/get-event-byorg/`, data, {
    headers: {
      "Content-Type": "multipart/form-data",
      "X-CSRFToken": token,
    },
    withCredentials: true,
  });
  console.log(response.data);
  return response.data;
}
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
export default function EditEvent({ searchParams }) {
  // console.log(searchParams);
  const [form, setForm] = useState({
    eventName: "",
    startDate: "",
    endDate: "",
    noVol: "",
    eventDesc: "",
    eventImage: undefined,
  });

  const [imgPreview, setImgPreview] = useState(
    form.eventImage
      ? "http://localhost:8000" + form.eventImage
      : "https://picsum.photos/200"
  );

  async function getEvent() {
    try {
      const response = await axios.get(
        `${API_HOST}/get-single-event/${searchParams.event}`,
        {
          withCredentials: true,
        }
      );
      response.data.startDate = response.data.startDate.substring(0, 16);
      response.data.endDate = response.data.endDate.substring(0, 16);
      console.log(response.data);
      setForm(response.data);
      if (response.data.eventImage) {
        setImgPreview("http://localhost:8000" + response.data.eventImage);
      }
    } catch (error) {
      console.error("There was an fetching your profile", error);
    }
  }
  useEffect(() => {
    getEvent();
  }, [searchParams]);

  function updateForm(value) {
    return setForm((prev) => {
      console.log(form);
      return { ...prev, ...value };
    });
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
            Edit Volunteering Event
          </Heading>
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
                <FormControl name="eventName" isRequired>
                  <FormLabel>Event Name</FormLabel>
                  <Input
                    name="eventName"
                    type="text"
                    value={form.eventName}
                    onChange={(e) => {
                      updateForm({ eventName: e.target.value });
                    }}
                  />
                </FormControl>
              </Box>
              <Box>
                <FormControl name="noVol" isRequired>
                  <FormLabel>Volunteers Needed</FormLabel>
                  <Input
                    name="noVol"
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
                <FormControl name="startDate" isRequired>
                  <FormLabel>Start Date</FormLabel>
                  <Input
                    name="startDate"
                    type="datetime-local"
                    value={form.startDate}
                    onChange={(e) => {
                      updateForm({ startDate: e.target.value });
                    }}
                  />
                </FormControl>
              </Box>
              <Box>
                <FormControl name="endDate" isRequired>
                  <FormLabel>End Date</FormLabel>
                  <Input
                    name="endDate"
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
            <FormControl id="eventImage">
              <FormLabel>Event Image</FormLabel>
              <Input
                name="eventImage"
                type="file"
                accept="image/png, image/jpeg"
                onChange={(e) => {
                  updateForm({ eventImage: e.target.files[0] });
                  setImgPreview(URL.createObjectURL(e.target.files[0]));
                }}
              />
              <Image src={imgPreview} />
            </FormControl>
            <FormControl id="eventDesc" isRequired>
              <FormLabel>Event Description</FormLabel>
              <Input
                name="eventDesc"
                type="text"
                value={form.eventDesc}
                onChange={(e) => {
                  updateForm({ eventDesc: e.target.value });
                }}
              />
            </FormControl>
            <Stack spacing={10} pt={2}>
              <ButtonGroup gap="4">
                <Link href="/dashboard" prefetch={false} replace={true}>
                  <Button
                    loadingText="Submitting"
                    size="lg"
                    bg={"blue.400"}
                    color={"white"}
                    _hover={{
                      bg: "blue.500",
                    }}
                    onClick={() => {
                      onSubmit(form);
                    }}
                  >
                    Update Event
                  </Button>
                </Link>
                <Link href="/dashboard" prefetch={false}>
                  <Button
                    size="lg"
                    bg={"red.400"}
                    color={"white"}
                    _hover={{
                      bg: "red.500",
                    }}
                  >
                    Cancel Update
                  </Button>
                </Link>
              </ButtonGroup>
            </Stack>
          </Stack>
        </Box>
      </Stack>
    </Flex>
  );
}
