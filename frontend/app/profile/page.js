"use client";

import {
  Flex,
  Box,
  FormControl,
  FormLabel,
  Input,
  InputGroup,
  HStack,
  InputRightElement,
  Stack,
  Button,
  Heading,
  Text,
  useColorModeValue,
  Link,
  Checkbox,
} from "../providers";
import { useState, useEffect } from "react";
import { ViewIcon, ViewOffIcon } from "../providers";
import { useToast } from "@chakra-ui/react";
import axios from "axios";

export default function ProfilePage() {
  // const [showPassword, setShowPassword] = useState(false);
  const API_HOST = "http://localhost:8000/api";
  const [details, setDetails] = useState({
    firstname: "",
    email: "",
    lastname: "",
    phoneNum: "",
    userName: "",
    nric: "",
    nokName: "",
    nokPhone: "",
    nokRelationship: "",
    birthday: "",
  });

  const updateDetails = (field, data) => {
    setDetails({
      ...details,
      [field]: data,
    });
  };

  let _csrfToken = null;
  const toast = useToast();
  useEffect(() => {
    getProfile();
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

  async function getProfile() {
    try {
      const response = await axios.get(`${API_HOST}/profile/`, {
        withCredentials: true,
      });
      setDetails({
        ...details,
        firstname: response.data["profile"]["user"]["first_name"],
        email: response.data["profile"]["user"]["email"],
        lastname: response.data["profile"]["user"]["last_name"],
        // nric : response.data["profile"]["user"]["nric"],
        phoneNum: response.data["profile"]["user"]["phoneNum"],
        userName: response.data["profile"]["user"]["username"],
        nokName: response.data["nok"]["name"],
        birthday: response.data["profile"]["birthday"],
        nokPhone: response.data["nok"]["phoneNum"],
        nokRelationship: response.data["nok"]["relationship"],
      });
      console.log(response);
      console.log(Date(details.birthday));
    } catch (error) {
      console.error("There was an fetching data", error);
    }
  }
  async function updateProfile() {
    const token = await getCsrfToken()
    console.log(token)
    try {
      console.log(details);
      response = await axios.put(`${API_HOST}/update-user-details/`, details, {
        withCredentials: true,
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": token,
        },
      });
      console.log(response)
      return response.data
    } catch (error) {
      console.log(error);
    }
  }

  return (
    <Flex
      minH={"100vh"}
      align={"center"}
      justify={"center"}
      bg={useColorModeValue("gray.50", "gray.800")}
    >
      <Stack spacing={8} mx={"auto"} maxW={"lg"} py={12} px={6}>
        <Stack align={"center"}>
          <Heading fontSize={"4xl"} textAlign={"center"}>
            User Profile
          </Heading>
          <Text fontSize={"lg"} color={"gray.600"}>
            My Details
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
                <FormControl id="firstName">
                  <FormLabel>First Name</FormLabel>
                  <Input
                    type="text"
                    onChange={(e) => updateDetails("firstname", e.target.value)}
                    value={details.firstname}
                  />
                </FormControl>
              </Box>
              <Box>
                <FormControl id="lastName">
                  <FormLabel>Last Name</FormLabel>
                  <Input type="text" value={details.lastname} />
                </FormControl>
              </Box>
            </HStack>
            <HStack>
              <Box>
                <FormControl id="phoneNum">
                  <FormLabel>Phone Number</FormLabel>
                  <Input type="tel" value={details.phoneNum} />
                </FormControl>
              </Box>
            </HStack>
            <FormControl id="email">
              <FormLabel>Email address</FormLabel>
              <Input type="email" value={details.email} />
            </FormControl>
            <Stack spacing={10} pt={2}>
              <Stack
                direction={{ base: "column", sm: "row" }}
                align={"start"}
                justify={"space-between"}
              >
                {/* <Checkbox>I am an Organisation</Checkbox> */}
                <FormControl id="email">
                  <FormLabel>Birthday</FormLabel>
                  <Input type="date" value={details.birthday} />
                </FormControl>
              </Stack>
              <Stack>
                <HStack>
                  <Box>
                    <FormControl id="nokName">
                      <FormLabel>NOK</FormLabel>
                      <Input type="text" value={details.nokName} />
                    </FormControl>
                  </Box>
                  <Box>
                    <FormControl id="relationship">
                      <FormLabel>Relationship</FormLabel>
                      <Input type="text" value={details.nokRelationship} />
                    </FormControl>
                  </Box>
                </HStack>

                <HStack>
                  <Box>
                    <FormControl id="phoneNum">
                      <FormLabel>Phone Number</FormLabel>
                      <Input type="tel" value={details.nokPhone} />
                    </FormControl>
                  </Box>
                </HStack>
              </Stack>
              <Button
                onClick={updateProfile}
                loadingText="Submitting"
                size="lg"
                bg={"blue.400"}
                color={"white"}
                _hover={{
                  bg: "blue.500",
                }}
              >
                Update Profile
              </Button>
            </Stack>
          </Stack>
        </Box>
      </Stack>
    </Flex>
  );
}
