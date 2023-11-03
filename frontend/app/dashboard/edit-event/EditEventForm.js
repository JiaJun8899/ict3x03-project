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
  useToast,
} from "@chakra-ui/react";
import React, { useState, useEffect } from "react";
import { useRouter } from "next/navigation";
import axios from "axios";
import Link from "next/link";
import { API_HOST, API_IMAGE, updateForm } from "@/app/utils/utils";
import Cookie from "js-cookie";

export default function EditEvent({ eventID }) {
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

  const [imgPreview, setImgPreview] = useState(
    form.eventImage ? API_IMAGE + form.eventImage : "https://picsum.photos/200"
  );

  async function getEvent() {
    try {
      const response = await axios.get(
        `${API_HOST}/get-single-event/${eventID}`,
        {
          withCredentials: true,
        }
      );
      response.data.startDate = response.data.startDate.substring(0, 16);
      response.data.endDate = response.data.endDate.substring(0, 16);
      setForm(response.data);
      if (response.data.eventImage) {
        setImgPreview(API_IMAGE + response.data.eventImage);
      }
    } catch (error) {
      console.error("There was an error getting the event");
    }
  }
  useEffect(() => {
    getEvent();
  }, [eventID]);

  async function onSubmit(data) {
    try {
      await axios.put(`${API_HOST}/get-event-byorg/`, data, {
        headers: {
          "Content-Type": "multipart/form-data",
          "X-CSRFToken": Cookie.get("csrftoken"),
        },
        withCredentials: true,
      });
      toast({
        title: `${form.eventName} Updated`,
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
            title: "Updated failed",
            description: values[0],
            status: "error",
            duration: 3000,
            isClosable: true,
          });
        }
      } else {
        toast({
          title: "Update failed",
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
                      updateForm({ eventName: e.target.value }, setForm);
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
                      updateForm({ noVol: e.target.value }, setForm);
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
                      updateForm({ startDate: e.target.value }, setForm);
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
                      updateForm({ endDate: e.target.value }, setForm);
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
                  updateForm({ eventImage: e.target.files[0] }, setForm);
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
                  updateForm({ eventDesc: e.target.value }, setForm);
                }}
              />
            </FormControl>
            <Stack spacing={10} pt={2}>
              <ButtonGroup gap="4">
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
