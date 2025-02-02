import { DetailsObj } from "@/lib/utils";
const BACKEND_ENDPOINT = "https://pills-recognition.onrender.com/analyze_pill";

export async function GET() {
  const res = await fetch(`${BACKEND_ENDPOINT}`);
  const data = await res.json();
  if (!data) {
    return new Response("Error", { status: 400 });
  } else if (data.length === 0) {
    return new Response("No data", { status: 404 });
  }

  return new Response(JSON.stringify(data[0]), { status: 200 });
}

export async function POST(request: Request): Promise<Response> {
  const body = await request.json();
  const res = await fetch(`${BACKEND_ENDPOINT}`, {
    method: "POST",
    body: JSON.stringify(body),
    headers: { "Content-Type": "application/json" },
  });

  if (!res.ok) {
    return new Response("Error", { status: 400 });
  }

  const data: DetailsObj[] = await res.json();
  if (!data) {
    return new Response("Error", { status: 400 });
  } else if (data.length === 0) {
    return new Response("No data", { status: 404 });
  }
  return new Response(JSON.stringify(data[0]), { status: 200 });
}
