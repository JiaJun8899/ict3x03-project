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
  Tooltip,
  useToast,
} from "../providers";
import { useState } from "react";
import { ViewIcon, ViewOffIcon } from "../providers";
import { useRouter } from "next/navigation";
import NextLink from "next/link";
import axios from "axios";
import ReCAPTCHA from "react-google-recaptcha-v2";
import { API_HOST, updateForm } from "@/app/utils/utils";

export default function SignupCard() {
  const [showPassword, setShowPassword] = useState(false);
  const [showPassword2, setShowPassword2] = useState(false);
  const router = useRouter();
  const [form, setForm] = useState({
    firstName: "",
    lastName: "",
    NRIC: "",
    phoneNum: "",
    birthday: "",
    organization: false,
    password: "",
    password2: "",
    email: "",
  });
  const [recaptchaValue, setRecaptchaValue] = useState(null);
  const toast = useToast();

  async function handleForm(form) {
    form.recaptchaValue = recaptchaValue;
    try {
      await axios.post(API_HOST + "/register", form);
      toast({
        title: "Account Created",
        status: "success",
        duration: 3000,
        isClosable: true,
      });
      router.replace("/");
    } catch (error) {
      if ("response" in error) {
        const values = Object.values(error.response.data);
        if (values[0] != "<") {
          toast({
            title: "Register failed",
            description: values[0],
            status: "error",
            duration: 3000,
            isClosable: true,
          });
        }
      } else {
        toast({
          title: "Register failed",
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
      <Stack spacing={8} mx={"auto"} maxW={"lg"} py={12} px={6}>
        <Stack align={"center"}>
          <Heading fontSize={"4xl"} textAlign={"center"}>
            Sign up
          </Heading>
          <Text fontSize={"lg"} color={"gray.600"}>
            Volunteer with us Today! ❤️
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
                <FormControl id="firstName" isRequired>
                  <FormLabel>First Name</FormLabel>
                  <Input
                    type="text"
                    value={form.firstName}
                    onChange={(e) => {
                      updateForm({ firstName: e.target.value }, setForm);
                    }}
                  />
                </FormControl>
              </Box>
              <Box>
                <FormControl id="lastName" isRequired>
                  <FormLabel>Last Name</FormLabel>
                  <Input
                    type="text"
                    value={form.lastName}
                    onChange={(e) => {
                      updateForm({ lastName: e.target.value }, setForm);
                    }}
                  />
                </FormControl>
              </Box>
            </HStack>
            <HStack>
              <Box>
                <FormControl id="nric" isRequired>
                  <FormLabel>NRIC (XXXA)</FormLabel>
                  <Input
                    type="text"
                    value={form.NRIC}
                    onChange={(e) => {
                      updateForm({ NRIC: e.target.value }, setForm);
                    }}
                  />
                </FormControl>
              </Box>
              <Box>
                <FormControl id="phoneNum" isRequired>
                  <FormLabel>Phone Number</FormLabel>
                  <Input
                    type="tel"
                    value={form.phoneNum}
                    onChange={(e) => {
                      updateForm({ phoneNum: e.target.value }, setForm);
                    }}
                  />
                </FormControl>
              </Box>
            </HStack>
            <FormControl id="email" isRequired>
              <FormLabel>Email address (username)</FormLabel>
              <Input
                type="email"
                value={form.email}
                onChange={(e) => {
                  updateForm({ email: e.target.value }, setForm);
                }}
              />
            </FormControl>
            <FormControl id="password" isRequired>
              <FormLabel>Password</FormLabel>
              <InputGroup>
                <Input
                  type={showPassword ? "text" : "password"}
                  value={form.password}
                  onChange={(e) => {
                    updateForm({ password: e.target.value }, setForm);
                  }}
                />
                <InputRightElement h={"full"}>
                  <Button
                    variant={"ghost"}
                    onClick={() =>
                      setShowPassword((showPassword) => !showPassword)
                    }
                  >
                    {showPassword ? <ViewIcon /> : <ViewOffIcon />}
                  </Button>
                </InputRightElement>
              </InputGroup>
            </FormControl>
            <FormControl id="password2" isRequired>
              <FormLabel>Confirm Password</FormLabel>
              <InputGroup>
                <Input
                  type={showPassword2 ? "text" : "password"}
                  value={form.password2}
                  onChange={(e) => {
                    updateForm({ password2: e.target.value }, setForm);
                  }}
                />
                <InputRightElement h={"full"}>
                  <Button
                    variant={"ghost"}
                    onClick={() =>
                      setShowPassword2((showPassword2) => !showPassword2)
                    }
                  >
                    {showPassword2 ? <ViewIcon /> : <ViewOffIcon />}
                  </Button>
                </InputRightElement>
              </InputGroup>
            </FormControl>
            <Stack spacing={10} pt={2}>
              <HStack
                direction={{ base: "column", sm: "row" }}
                align={"start"}
                justify={"space-between"}
              >
                <FormControl>
                  <FormLabel>Organization</FormLabel>
                  <Checkbox
                    value={form.organization}
                    onChange={(e) => {
                      updateForm({ organization: e.target.checked }, setForm);
                    }}
                  >
                    I am an Organisation
                  </Checkbox>
                </FormControl>
                <FormControl
                  id="email"
                  isRequired={form.organization ? false : true}
                >
                  <FormLabel>Birthday if applicable</FormLabel>
                  <Tooltip
                    label="You must be 16 years old and above to volunteer with us"
                    hasArrow
                  >
                    <Input
                      disabled={form.organization ? true : false}
                      type="date"
                      max={
                        new Date(
                          new Date().setFullYear(new Date().getFullYear() - 16)
                        )
                          .toISOString()
                          .split("T")[0]
                      }
                      value={form.birthday}
                      onChange={(e) => {
                        updateForm({ birthday: e.target.value }, setForm);
                      }}
                    />
                  </Tooltip>
                </FormControl>
              </HStack>
              <FormControl id="recaptcha" isRequired>
                <ReCAPTCHA
                  sitekey="6Ldqu7YoAAAAAOWypyZABbjPTmRyb7KIv7gYs4j4"
                  onChange={(value) => {
                    setRecaptchaValue(value);
                  }}
                />
              </FormControl>
              <Button
                loadingText="Submitting"
                size="lg"
                bg={"blue.400"}
                color={"white"}
                _hover={{
                  bg: "blue.500",
                }}
                onClick={() => {
                  handleForm(form);
                }}
              >
                Sign up
              </Button>
            </Stack>
            <Stack pt={6}>
              <Text align={"center"}>
                Already a user?{" "}
                <Link as={NextLink} color={"blue.400"} href="/login">
                  Login
                </Link>
              </Text>
            </Stack>
          </Stack>
        </Box>
      </Stack>
    </Flex>
  );
}
