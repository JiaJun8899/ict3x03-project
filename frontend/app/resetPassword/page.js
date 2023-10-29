'use client'
import React, { useState } from 'react';
import { useRouter } from "next/navigation";
import {
  Button,
  FormControl,
  Flex,
  Heading,
  Input,
  Stack,
  Text,
} from '@chakra-ui/react';
import axios from "axios";
import { useToast } from "@chakra-ui/react";
import Cookie from "js-cookie";

export default function ForgotPasswordForm() {
    const [email, setEmail] = useState('');
    const toast = useToast();
  const [otp, setOtp] = useState('');
  const [newPassword, setNewPassword] = useState('');
  const [confirmPassword, setConfirmPassword] = useState('');

    const router = useRouter(); // Get the router object
    const API_HOST = `http://localhost:8000/api`;

const handleSubmitRequest = async () => {
  try {
    // Validate whether newPassword and confirmPassword are the same, or any other validations
    if (newPassword !== confirmPassword) {
      // Show some toast or error message
      return;
    }

    const response = await axios.put(
      `${API_HOST}/auth-reset-password/`,
      {
        OTP: otp,
        email:email,
        newPassword: newPassword,
        newPasswordConfirmation: confirmPassword,
      },
      {
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": Cookie.get("csrftoken"),
        },
        withCredentials: true,
      }
    );

    if (response.status === 200) {
      // Handle success - Maybe redirect to login or show a success message
        router.push("/login")
    }
  } catch (error) {
    toast({
        title: "Failed to change password",
        description: "Fail to change password",
        status: "error",
        duration: 3000,
        isClosable: true,
    });
  }
};

    const handleRequestOtp = async () => {
            const response = await axios.post(
                `${API_HOST}/auth-reset-password/`,
                {
                    "email":email
                },
                {
                    headers: {
                        "X-CSRFToken": Cookie.get("csrftoken"),
                        "Content-Type": "application/json",
                    },
                    withCredentials: true,
                }
            );

            if (response.status === 200) {
                toast({
                    title: "OTP Sent.",
                    description: "Check your email for the OTP!",
                    status: "success",
                    duration: 3000,
                    isClosable: true,
                });
            }
    };

  return (
    <Flex minH={'100vh'} align={'center'} justify={'center'}>
      <Stack spacing={4} w={'full'} maxW={'md'} p={6} my={12}>
        <Heading fontSize={{ base: '2xl', md: '3xl' }}>
          Forgot your password?
        </Heading>
        <Text fontSize={{ base: 'sm', sm: 'md' }}>
          You'll get an email with a reset link
        </Text>
      
        {/* Email input field */}

        {/* OTP input field */}
        <Flex alignItems="center">
        <FormControl id="email">
            <Input
                type="email"
                placeholder="Your Email"
                value={email}
                onChange={(e) => setEmail(e.target.value)}
            />
        </FormControl>
          <Button bg={'blue.400'} color={'white'} onClick={handleRequestOtp}>
            GET OTP
          </Button>
        </Flex>

          <FormControl id="otp" mr={4}>
            <Input
              type="text"
              placeholder="Enter OTP"
              value={otp}
              onChange={(e) => setOtp(e.target.value)}
            />
          </FormControl>

        {/* New Password input field */}
        <FormControl id="new-password">
          <Input
            type="password"
            placeholder="New Password"
            value={newPassword}
            onChange={(e) => setNewPassword(e.target.value)}
          />
        </FormControl>

        {/* Confirm New Password input field */}
        <FormControl id="confirm-password">
          <Input
            type="password"
            placeholder="Confirm New Password"
            value={confirmPassword}
            onChange={(e) => setConfirmPassword(e.target.value)}
          />
        </FormControl>

        {/* Buttons */}
        <Stack spacing={4}>
          <Button bg={'green.400'} color={'white'} onClick={handleSubmitRequest}>
            Submit Request
          </Button>
        </Stack>
      </Stack>
    </Flex>
  );
}

