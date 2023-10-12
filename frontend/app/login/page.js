'use client'
import {useState} from "react"
import { useToast } from '@chakra-ui/react'
import {
  Flex,
  Box,
  FormControl,
  FormLabel,
  Input,
  Checkbox,
  Stack,
  Button,
  Heading,
  Text,
  useColorModeValue,
} from '@chakra-ui/react'

export default function SimpleCard() {
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const toast = useToast();
    const API_HOST = `http://localhost:8000/api`;

  const handleLogin = async () => {
    try {
      const response = await fetch(`${API_HOST}/auth-login/`, {

        method: 'POST',
        headers: { 'Content-Type': 'application/json','X-CSRFToken': await getCsrfToken()},
          body: JSON.stringify({ "username":email,"password":password} 
),
        credentials: 'include',
      });

      if (response.ok) {
        toast({
          title: "Login successful.",
          description: "You are now logged in!",
          status: "success",
          duration: 3000,
          isClosable: true,
        });
        // Redirect to dashboard or wherever you want
      } else {
        toast({
          title: "Login failed.",
          description: await response.text(),
          status: "error",
          duration: 3000,
          isClosable: true,
        });
      }
    } catch (error) {
      console.error("There was an error logging in", error);
    }
  };

    let _csrfToken = null;

    async function getCsrfToken() {
      if (_csrfToken === null) {
        const response = await fetch(`${API_HOST}/csrf/`, {
          credentials: 'include',
        });
        const data = await response.json();
        _csrfToken = data.csrfToken;
      }
      return _csrfToken;
    }

    async function testRequest(method) {
      const response = await fetch(`${API_HOST}/ping/`, {
        method: method,
        headers: (
          method === 'POST'
            ? {'X-CSRFToken': await getCsrfToken()}
            : {}
        ),
        credentials: 'include',
      });
      const data = await response.json();
      return data.result;
    }



  return (
    <Flex
      minH={'100vh'}
      align={'center'}
      justify={'center'}
      bg={useColorModeValue('gray.50', 'gray.800')}>
      <Stack spacing={8} mx={'auto'} maxW={'lg'} py={12} px={6}>
        <Stack align={'center'}>
          <Heading fontSize={'4xl'}>Sign in to your account</Heading>
          <Text fontSize={'lg'} color={'gray.600'}>
            to enjoy all of our cool <span color={'blue.400'}>features</span> ✌️
          </Text>
        </Stack>
        <Box
          rounded={'lg'}
          bg={useColorModeValue('white', 'gray.700')}
          boxShadow={'lg'}
          p={8}>
      <form>
          <Stack spacing={4}>
            <FormControl id="email">
              <FormLabel>Email address</FormLabel>
              <Input type="email" value={email}  onChange={(e) => setEmail(e.target.value)}/>
            </FormControl>
            <FormControl id="password">
              <FormLabel>Password</FormLabel>
              <Input type="password" value={password}  onChange={(e) => setPassword(e.target.value)}/>
            </FormControl>
            <Stack spacing={10}>
              <Stack
                direction={{ base: 'column', sm: 'row' }}
                align={'start'}
                justify={'space-between'}>
                <Checkbox>Remember me</Checkbox>
                <Text color={'blue.400'}>Forgot password?</Text>
              </Stack>
              <Button
                onClick={handleLogin}
                bg={'blue.400'}
                color={'white'}
                _hover={{
                  bg: 'blue.500',
                }}>
                Sign in
              </Button>
            </Stack>
          </Stack>
        </form>
        </Box>
      </Stack>
    </Flex>
  )
}
