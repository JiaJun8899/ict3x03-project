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
} from "../providers";
import { useState, useEffect, Suspense } from "react";
import axios from "axios";
import { API_HOST, getRole } from "@/app/utils/utils";
import { notFound } from "next/navigation";
import Cookie from "js-cookie";

export default function ProfilePage() {
  const [userRole, setUserRole] = useState("none");
  const [loading, setLoading] = useState(true);    
  useEffect(() => {
    getRole(setUserRole,setLoading);
  }, []);
  
  function EditProfile(){
    const role = userRole.role;
    if(role !== 'Organizer' && role !== "Normal"){
      return notFound();
    }
    const [details, setDetails] = useState({
      first_name: "",
      email: "",
      last_name: "",
      phoneNum: "",
      username: "",
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
  
    const toast = useToast();
    useEffect(() => {
      getProfile();
    }, []);
  
    async function getProfile() {
      try {
        const response = await axios.get(`${API_HOST}/profile/`, {
          withCredentials: true,
        });
        setDetails({
          ...details,
          first_name: response.data["profile"]["user"]["first_name"],
          email: response.data["profile"]["user"]["email"],
          last_name: response.data["profile"]["user"]["last_name"],
          phoneNum: response.data["profile"]["user"]["phoneNum"],
          username: response.data["profile"]["user"]["username"],
          birthday: response.data["profile"]["birthday"],
        });
        if (response.data["nok"]) {
          setDetails({
            ...details,
            first_name: response.data["profile"]["user"]["first_name"],
            email: response.data["profile"]["user"]["email"],
            last_name: response.data["profile"]["user"]["last_name"],
            phoneNum: response.data["profile"]["user"]["phoneNum"],
            username: response.data["profile"]["user"]["username"],
            birthday: response.data["profile"]["birthday"],
            nokName: response.data["nok"]["name"],
            nokPhone: response.data["nok"]["phoneNum"],
            nokRelationship: response.data["nok"]["relationship"],
          });
        }
      } catch (error) {
        console.error("There was an fetching your profile", error);
      }
    }
    async function updateProfile() {
      try {
        const response = await axios.put(
          `${API_HOST}/update-user-details/`,
          details,
          {
            withCredentials: true,
            headers: {
              "Content-Type": "application/json",
              "X-CSRFToken": Cookie.get("csrftoken"),
            },
          }
        );
        console.log(response);
        toast({
          title: "Profile updated successful.",
          status: "success",
          duration: 3000,
          isClosable: true,
        });
      } catch (error) {
        console.log(error);
        toast({
          title: "Profile update failed.",
          status: "error",
          duration: 3000,
          isClosable: true,
        });
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
                    <Input
                      type="text"
                      value={details.lastname}
                      onChange={(e) => updateDetails("lastname", e.target.value)}
                    />
                  </FormControl>
                </Box>
              </HStack>
              <HStack>
                <Box>
                  <FormControl id="phoneNum">
                    <FormLabel>Phone Number</FormLabel>
                    <Input
                      type="tel"
                      value={details.phoneNum}
                      onChange={(e) => updateDetails("phoneNum", e.target.value)}
                    />
                  </FormControl>
                </Box>
              </HStack>
              <FormControl id="email">
                <FormLabel>Email address</FormLabel>
                <Input
                  type="email"
                  value={details.email}
                  onChange={(e) => updateDetails("email", e.target.value)}
                />
              </FormControl>
              <Stack spacing={10} pt={2}>
                <Stack
                  direction={{ base: "column", sm: "row" }}
                  align={"start"}
                  justify={"space-between"}
                >
                  <FormControl id="email">
                    <FormLabel>Birthday</FormLabel>
                    <Input
                      type="date"
                      value={details.birthday}
                      onChange={(e) => updateDetails("birthday", e.target.value)}
                    />
                  </FormControl>
                </Stack>
                <Stack>
                  <HStack>
                    <Box>
                      <FormControl id="nokName">
                        <FormLabel>NOK</FormLabel>
                        <Input
                          type="text"
                          value={details.nokName}
                          onChange={(e) =>
                            updateDetails("nokName", e.target.value)
                          }
                        />
                      </FormControl>
                    </Box>
                    <Box>
                      <FormControl id="relationship">
                        <FormLabel>Relationship</FormLabel>
                        <Input
                          type="text"
                          value={details.nokRelationship}
                          onChange={(e) =>
                            updateDetails("nokRelationship", e.target.value)
                          }
                        />
                      </FormControl>
                    </Box>
                  </HStack>
  
                  <HStack>
                    <Box>
                      <FormControl id="phoneNum">
                        <FormLabel>Phone Number</FormLabel>
                        <Input
                          type="tel"
                          value={details.nokPhone}
                          onChange={(e) =>
                            updateDetails("nokPhone", e.target.value)
                          }
                        />
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
  return(
    <div>
      <Suspense fallback={<p>Loading ...</p>}>
        {loading ? (
          <p>Building dashboard...</p>
        ) : (
          <EditProfile userRole={userRole} />
        )}
      </Suspense>
    </div>
  )

}
