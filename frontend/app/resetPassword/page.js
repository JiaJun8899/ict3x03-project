'use client'
import React, { useState } from 'react';
import {
  Button,
  FormControl,
  Flex,
  Heading,
  Input,
  Stack,
  Text,
  useColorModeValue,
} from '@chakra-ui/react';
import Cookie from "js-cookie";
import axios from "axios";
import { useToast } from "@chakra-ui/react";
export default function ForgotPasswordForm() {
    const toast = useToast();
    const [email, setEmail] = useState('');
    const [otp, setOtp] = useState('');
    const [isOtpStage, setIsOtpStage] = useState(false);
    const API_HOST = `http://localhost:8000/api`;
  
    const handleLogin = async () => {
        await handleRequestOtp();
        toast({
            title: "OTP Sent.",
            description: "Check your email for the OTP!",
            status: "success",
            duration: 3000,
            isClosable: true,
        });
    };
    const handleButtonClick = () => {
        if (isOtpStage) {
            verifyOTP();
        } else {
            handleLogin();
            setIsOtpStage(true);
        }
    };

    const handleRequestOtp = async () => {
        try {
            const response = await axios.post(
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

            if (response.status === 200) {
                setOtpSent(true);
                toast({
                    title: "OTP Sent.",
                    description: "Check your email for the OTP!",
                    status: "success",
                    duration: 3000,
                    isClosable: true,
                });
            }
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
            const response = await axios.post(
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

            if (response.status === 200) {
                setOtpSent(true);
                toast({
                    title: "OTP Verification.",
                    description: "LOGIN COMPLETE",
                    status: "success",
                    duration: 3000,
                    isClosable: true,
                });
                router.push("/dashboard"); // Redirect to dashboard
            }
        } catch (error) {
            console.log(error);
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
    <Flex minH={'100vh'} align={'center'} justify={'center'} bg={useColorModeValue('gray.50', 'gray.800')}>
      <Stack spacing={4} w={'full'} maxW={'md'} bg={useColorModeValue('white', 'gray.700')} rounded={'xl'} boxShadow={'lg'} p={6} my={12}>
        <Heading lineHeight={1.1} fontSize={{ base: '2xl', md: '3xl' }}>
          {isOtpStage ? 'Verify OTP' : 'Forgot your password?'}
        </Heading>
        <Text fontSize={{ base: 'sm', sm: 'md' }} color={useColorModeValue('gray.800', 'gray.400')}>
          {isOtpStage ? 'Enter the OTP sent to your email' : "You'll get an email with a reset link"}
        </Text>
        {!isOtpStage && (
          <FormControl id="email">
            <Input
              placeholder="your-email@example.com"
              _placeholder={{ color: 'gray.500' }}
              type="email"
              value={email}
              onChange={(e) => setEmail(e.target.value)}
            />
          </FormControl>
        )}
        {isOtpStage && (
          <FormControl id="otp">
            <Input
              placeholder="Enter OTP"
              _placeholder={{ color: 'gray.500' }}
              type="text"
              value={otp}
              onChange={(e) => setOtp(e.target.value)}
            />
          </FormControl>
        )}
        <Stack spacing={6}>
          <Button
            bg={'blue.400'}
            color={'white'}
            _hover={{
              bg: 'blue.500',
            }}
            onClick={handleButtonClick}
          >
            {isOtpStage ? 'Verify OTP' : 'Request OTP'}
          </Button>
        </Stack>
      </Stack>
    </Flex>
  );
}
