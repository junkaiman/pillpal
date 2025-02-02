"use client";
import Image from "next/image";
import { DetailsObj } from "@/lib/utils";
import DialogWithButton from "./DialogWithButton";
import { useSpeech } from "react-text-to-speech";
interface IDetailsProps {
  data: DetailsObj;
}

export default function Details({ data }: IDetailsProps) {
  const {} = useSpeech({
    text: data.description,
    pitch: 1.4,
    rate: 0.5,
    volume: 1,
    lang: "en-US",
    voiceURI: "com.apple.eloquence.en-US.Grandpa",
    autoPlay: true,
    highlightText: false,
    showOnlyHighlightedText: false,
    highlightMode: "word",
  });

  return (
    <div className="flexflex-col min-h-screen">
      <div className="p-5 mt-3">
        <h1 className="mb-3 text-3xl font-bold">Summary</h1>
        <Image
          src={data.imgUrl}
          alt="Image"
          width={300}
          height={300}
          className="rounded-lg"
        ></Image>
        <p className="text-lg text-gray-700 leading-relaxed">
          {data.description}
        </p>
        <div className="my-5 flex flex-row space-x-3">
          <DialogWithButton
            buttonText="Interactions"
            title="Interactions"
            description={data.interactions}
            type="interactions"
          />
          <DialogWithButton
            buttonText="Side Effects"
            title="Side Effects"
            description={data.sideEffects}
            type="sideEffects"
          />
        </div>
      </div>
    </div>
  );
}
