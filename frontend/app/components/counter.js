"use client";

import { useState } from "react";

export const Counter = () => {
  const [count, setCount] = useState(0);

  return (
    <div>
      <p>{count}</p>

      <button onClick={() => setCount((x) => x + 1)}>{count} + 1</button>
    </div>
  );
};
