"use client";
import { useState } from "react";
import { useRouter } from "next/navigation";
import {
  Flex,
  Box,
  FormControl,
  FormLabel,
  Input,
  useToast,
  Stack,
  Button,
  Heading,
  Text,
  useColorModeValue,
} from "@chakra-ui/react";
import Cookie from "js-cookie";
import axios from "axios";
import { API_HOST } from "@/app/utils/utils";

export default function LoginPage() {
  const [otp, setOtp] = useState("");
  const router = useRouter(); // Get the router object
  const [otpSent, setOtpSent] = useState(false);
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const toast = useToast();

  const handleLogin = async () => {
    try {
      await axios.post(
        `${API_HOST}/auth-login/`,
        { username: email, password: password },
        {
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": Cookie.get("csrftoken"),
          },
          withCredentials: true,
        }
      );
      const otpResponse = await handleRequestOtp();
    } catch (error) {
      toast({
        title: "Login failed.",
        description: "Invalid credentials", // Assuming the server returns the error description in the response data
        status: "error",
        duration: 3000,
        isClosable: true,
      });
    }
  };
  const handleButtonClick = () => {
    if (otpSent) {
      verifyOTP();
    } else {
      handleLogin();
    }
  };

  const handleRequestOtp = async () => {
    try {
      await axios.post(
        `${API_HOST}/auth-get-OTP/`,
        {},
        {
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": Cookie.get("csrftoken"),
          },
          withCredentials: true,
        }
      );
      setOtpSent(true);
      toast({
        title: "OTP Sent.",
        description: "Check your email for the OTP!",
        status: "success",
        duration: 3000,
        isClosable: true,
      });
    } catch (error) {
      toast({
        title: "OTP Sent.",
        description: "Fail to sent otp to cilent",
        status: "error",
        duration: 3000,
        isClosable: true,
      });
    }
  };

  const verifyOTP = async () => {
    try {
      await axios.post(
        `${API_HOST}/auth-verify-OTP/`,
        { OTP: otp },
        {
          headers: {
            "Content-Type": "application/json",
            "X-CSRFToken": Cookie.get("csrftoken"),
          },
          withCredentials: true,
        }
      );
      setOtpSent(true);
      toast({
        title: "OTP Verification.",
        description: "LOGIN COMPLETE",
        status: "success",
        duration: 3000,
        isClosable: true,
      });
      router.push("/dashboard"); // Redirect to dashboard
    } catch (error) {
      console.error("Error Verifying OTP");
      toast({
        title: "OTP Verification.",
        description: "OTP WRONG",
        status: "error",
        duration: 3000,
        isClosable: true,
      });
    }
  };
  return (
    <Flex
      minH={"100vh"}
      align={"center"}
      justify={"center"}
      bg={useColorModeValue("gray.50", "gray.800")}
    >
      <Stack spacing={8} mx={"auto"} maxW={"lg"} py={12} px={6}>
        <Stack align={"center"}>
          <Heading fontSize={"4xl"}>Sign in to your account</Heading>
          <Text fontSize={"lg"} color={"gray.600"}>
            to enjoy all of our cool <span color={"blue.400"}>features</span> ✌️
          </Text>
        </Stack>
        <Box
          rounded={"lg"}
          bg={useColorModeValue("white", "gray.700")}
          boxShadow={"lg"}
          p={8}
        >
          <form>
            <Stack spacing={4}>
              <FormControl id="email">
                <FormLabel>Email address</FormLabel>
                <Input
                  type="email"
                  value={email}
                  onChange={(e) => setEmail(e.target.value)}
                />
              </FormControl>
              <FormControl id="password">
                <FormLabel>Password</FormLabel>
                <Input
                  type="password"
                  value={password}
                  onChange={(e) => setPassword(e.target.value)}
                />
              </FormControl>
              <Stack spacing={4}>
                {otpSent && (
                  <FormControl id="otp">
                    <FormLabel>Enter OTP</FormLabel>
                    <Input
                      type="text"
                      value={otp}
                      onChange={(e) => setOtp(e.target.value)}
                    />
                  </FormControl>
                )}
                <Button
                  onClick={handleButtonClick}
                  bg={"blue.400"}
                  color={"white"}
                >
                  {otpSent ? "Verify OTP" : "Request OTP"}
                </Button>
                <Button
                  variant={"link"}
                  colorScheme={"blue"}
                  size={"sm"}
                  onClick={() => {
                    router.push("/resetPassword");
                  }}
                >
                  Forgot your password!?!
                </Button>
                <Button
                  variant={"link"}
                  colorScheme={"blue"}
                  size={"sm"}
                  onClick={() => {
                    router.push("/register");
                  }}
                >
                  New? Register with us today!
                </Button>
              </Stack>
            </Stack>
          </form>
        </Box>
      </Stack>
    </Flex>
  );
}
