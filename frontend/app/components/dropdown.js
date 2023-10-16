"use client";

import { usePathname, useRouter, useSearchParams } from "next/navigation";

const options = ["mew", "mewtwo", "pikachu"];

export const DropDown = ({ selected }) => {
  const router = useRouter();
  const pathname = usePathname();
  const searcParams = useSearchParams();

  const onSelect = (event) => {
    const current = new URLSearchParams(searcParams);

    const value = event.target.value.trim();

    if (!value) {
      current.delete("selected");
    } else {
      current.set("selected", event.target.value);
    }

    const search = current.toString();
    const query = search ? `?${search}` : "";

    router.push(`${pathname}${query}`);
  };

  return (
    <select value={selected} onChange={onSelect}>
      <option value="">None</option>
      {options.map((opt) => (
        <option key={opt} value={opt}>
          {opt}
        </option>
      ))}
    </select>
  );
};
