import { DetailsObj } from "@/lib/utils";
export function test() {
  return fetch("/api");
}

export async function uploadPhoto(file: File): Promise<DetailsObj> {
  // transform file to base64
  const reader = new FileReader();
  reader.readAsDataURL(file);
  const base64data = await new Promise<string>((resolve) => {
    reader.onloadend = () => {
      // const base64 = reader.result as string;
      const base64 = (reader.result as string).replace(
        /^data:image\/[a-z]+;base64,/,
        ""
      );
      resolve(base64);
    };
  });

  // send request to server
  const response = await fetch("/api", {
    method: "POST",
    body: JSON.stringify({ image: base64data }),
    headers: {
      "Content-Type": "application/json",
    },
  });
  if (!response.ok) {
    throw new Error(await response.text());
  }

  const result: DetailsObj = await response.json();
  return result;
}
