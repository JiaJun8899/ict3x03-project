"use client";
import { DateTime } from "luxon";
import axios from "axios";

export const API_HOST = "https://silly-borg.cloud/api";
export const API_IMAGE = "https://silly-borg.cloud";

export function updateForm(value, setter, theUse) {
  return setter((prev) => {
    return { ...prev, ...value };
  });
}

export function convertTime(time) {
  const convertedTime = DateTime.fromISO(time)
    .toJSDate()
    .toLocaleString("en-SG");
  return convertedTime;
}

export async function getRole(setUserRole, setLoading) {
  try {
    const response = await axios.get(`${API_HOST}/check-auth`, {
      withCredentials: true,
    });
    setUserRole(response.data);
  } catch (error) {
    console.error("Error getting your Role")
  } finally {
    setLoading(false);
  }
}
