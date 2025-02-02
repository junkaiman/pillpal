"use client";

import React, { useState, useEffect } from "react";
import { test } from "@/app/api/utils";

export default function TestComponent() {
  const [data, setData] = useState("");

  useEffect(() => {
    test()
      .then((res) => res.json())
      .then(setData);
  }, []);

  return (
    <div>
      <h1 className="text-4xl font-bold text-center">Test Component</h1>
      <p className="text-center">{JSON.stringify(data)}</p>
    </div>
  );
}
