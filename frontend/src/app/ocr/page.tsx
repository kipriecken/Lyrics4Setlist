"use client";

import React, { useState } from "react";
import { createWorker } from "tesseract.js";

const OcrReader = () => {
  const [image, setImage] = useState<File | null>(null);
  const [text, setText] = useState<string>("");

  const readImage = async () => {
    if (!image) return;

    const worker = await createWorker("eng");
    const {
      data: { text },
    } = await worker.recognize(image);
    setText(text);
    await worker.terminate();
  };

  return (
    <div className="flex min-h-screen items-center justify-center bg-zinc-50 font-sans dark:bg-black">
      <div className="flex min-h-screen max-w-3xl flex-col items-center justify-between py-32 px-16 bg-white dark:bg-black sm:items-start">
        <input
          type="file"
          //   accept="image/*"
          onChange={(e) => setImage(e.target.files?.[0] || null)}
          className="block w-full text-sm text-gray-500
  file:mr-4 file:py-2 file:px-4
  file:rounded-full file:border-0
  file:text-sm file:font-semibold
  file:bg-violet-50 file:text-violet-700
  hover:file:bg-violet-100"
        />
        <button
          onClick={readImage}
          className="mt-6 rounded bg-blue-500 px-4 py-2 text-white hover:bg-blue-600 disabled:bg-gray-400 disabled:cursor-not-allowed"
        >
          Read Image
        </button>
        <p className=" bg-amber-50 text-black">{text}</p>
      </div>
    </div>
  );
};

export default OcrReader;
