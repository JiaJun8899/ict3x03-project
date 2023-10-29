"use client";

import {
  Box,
  Flex,
  Avatar,
  Text,
  Button,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
  MenuDivider,
  useDisclosure,
  useColorModeValue,
  Stack,
  useColorMode,
  Center,
  useToast,
} from "../providers";
import NextLink from "next/link";
import axios from "axios";
import { MoonIcon, SunIcon } from "../providers";
import { API_HOST } from "@/app/utils/utils";

const NavLink = (props) => {
  const { children } = props;

  return (
    <Box
      as="a"
      px={2}
      py={1}
      rounded={"md"}
      _hover={{
        textDecoration: "none",
        bg: useColorModeValue("gray.200", "gray.700"),
      }}
      href={"#"}
    >
      {children}
    </Box>
  );
};



export default function Nav() {
  const { colorMode, toggleColorMode } = useColorMode();
  const { isOpen, onOpen, onClose } = useDisclosure();
  let _csrfToken = null;
  const toast = useToast();

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
  
  async function logout() {
    const token = await getCsrfToken();
    var response = await axios
      .post(`${API_HOST}/auth-logout/`,{}, {
        withCredentials: true,
        headers: {
          "Content-Type": "application/json",
          "X-CSRFToken": token,
        },
      })
      .then(function (response) {
        console.log(response);
        toast({
          title: "Logout successful.",
          // description: "You are now logged in!",
          status: "success",
          duration: 3000,
          isClosable: true,
        });
      })
      .catch(function (error) {
        console.log(error);
        toast({
          title: "Logout failed.",
          // description: await response.text(),
          status: "error",
          duration: 3000,
          isClosable: true,
        });
      });
  }

  return (
    <>
      <Box bg={useColorModeValue("gray.100", "gray.900")} px={4}>
        <Flex h={16} alignItems={"center"} justifyContent={"space-between"}>
          {/* <Box>Logo</Box> */}
          <NextLink href={`/dashboard/`}>
            <Button variant={"link"}>Dashboard</Button>
          </NextLink>

          <Flex alignItems={"center"}>
            <Stack direction={"row"} spacing={7}>
              <Button onClick={toggleColorMode}>
                {colorMode === "light" ? <MoonIcon /> : <SunIcon />}
              </Button>

              <Menu>
                <MenuButton
                  as={Button}
                  rounded={"full"}
                  variant={"link"}
                  cursor={"pointer"}
                  minW={0}
                >
                  <Avatar
                    size={"sm"}
                    src={"https://avatars.dicebear.com/api/male/username.svg"}
                  />
                </MenuButton>
                <MenuList alignItems={"center"}>
                  <br />
                  <Center>
                    <Avatar
                      size={"2xl"}
                      src={"https://avatars.dicebear.com/api/male/username.svg"}
                    />
                  </Center>
                  <br />
                  <Center>
                    <p>Username</p>
                  </Center>
                  <br />
                  <MenuDivider />
                  {/* <MenuItem>Your Servers</MenuItem> */}
                  <NextLink href={`/profile/`}>
                    <MenuItem>Account Settings</MenuItem>
                  </NextLink>
                  <NextLink href={`/login/`}>
                  <MenuItem onClick={logout}>Logout</MenuItem>
                  </NextLink>
                </MenuList>
              </Menu>
            </Stack>
          </Flex>
        </Flex>
      </Box>
    </>
  );
}
